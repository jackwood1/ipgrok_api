"""
This module provides the API endpoint for comparing benefits data between two files.
It includes functions for reading, processing, cleansing, validating, normalizing, merging data,
generating responses, and consolidating and ordering the response.

Functions:
- read_file(file): Reads the content of the uploaded file and returns a DataFrame.
- process_files(file1, file2): Processes the uploaded files and returns DataFrames for enrollment and partner data.
- cleanse_data(df_symetra, df_partner): Cleanses the data by normalizing and formatting columns.
- validate_and_normalize_data(df_symetra, df_partner): Validates and normalizes the data based on predefined rules.
- merge_dataframes(df_symetra, df_partner): Merges the dataframes and identifies records unique to each file.
- generate_response(df_merged, df_only_in_enrollment, df_only_in_other): Generates the response by identifying changes.
- consolidate_and_order_response(response): Consolidates and orders the response data.
- benefits_compare(request, file1, file2): API endpoint for comparing benefits data between two files.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Query
import logging
import pandas as pd
import io
import numpy as np
import json
import re
from app.config import (
    partner_fields,
    core_product_names,
    core_product_attribs,
    partner_product_names,
    partner_product_attrs,
    enrollment_fields,
    extended_bases_attribs,
    base_matching_attribs,
    sort_fixed_columns,
    sort_match_columns,
    drop_columns
)
from app.utils import (
    normalize_gender,
    normalize_phone_number,
    normalize_and_validate_dollar_amount,
    validate_and_normalize_date,
    normalize_email,
    validate_and_normalize_names,
    validate_and_normalize_string
)

router = APIRouter()
logger = logging.getLogger("benefits_compare")

async def read_file(file: UploadFile):
    """
    Reads the content of the uploaded file and returns a DataFrame.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        DataFrame: The content of the file as a DataFrame.
    """
    logger.debug(f"Reading file: {file.filename}")
    file_content = await file.read()
    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(io.BytesIO(file_content))
    else:
        logger.error("Unsupported file type")
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return df, file_content

async def process_files(file1: UploadFile, file2: UploadFile):
    """
    Processes the uploaded files and returns DataFrames for enrollment and partner data.

    Args:
        file1 (UploadFile): The first uploaded file.
        file2 (UploadFile): The second uploaded file.

    Returns:
        tuple: DataFrames for enrollment and partner data.
    """
    logger.debug(f"Processing files: {file1.filename}, {file2.filename}")
    file1_content = await file1.read()
    file2_content = await file2.read()

    if file1.filename.startswith("Enrollment"):
        enrollment_file_content = file1_content
        other_file_content = file2_content
        enrollment_filename = file1.filename
        other_filename = file2.filename
    elif file2.filename.startswith("Enrollment"):
        enrollment_file_content = file2_content
        other_file_content = file1_content
        enrollment_filename = file2.filename
        other_filename = file1.filename
    else:
        logger.error("No file starts with 'Enrollment'")
        raise HTTPException(status_code=400, detail="No file starts with 'Enrollment'")

    logger.debug("Mapping columns for enrollment and other files")
    enrollment_file_content_str = enrollment_file_content.decode('utf-8')
    other_file_content_str = other_file_content.decode('utf-8')

    first_line_f1 = enrollment_file_content_str.split('\n')[0].strip()
    columns_f1 = first_line_f1.split(',')
    mapped_columns_f1 = [enrollment_fields.get(col, [col])[0] for col in columns_f1]
    enrollment_file_content_str = enrollment_file_content_str.replace(first_line_f1, ','.join(mapped_columns_f1))

    first_line_f2 = other_file_content_str.split('\n')[0].strip()
    columns_f2 = first_line_f2.split(',')

    i = 0
    while i < len(columns_f2):
        col = columns_f2[i]
        if col in partner_product_names:
            replacement_made = False
            for j in range(i + 1, len(columns_f2)):
                if columns_f2[j] in partner_product_attrs:
                    columns_f2[j] = partner_product_attrs[columns_f2[j]].replace("REPLACE", col)
                    replacement_made = True
                else:
                    break
            if not replacement_made:
                i = j
            else:
                i += 1
        else:
            i += 1

    mapped_columns_f2 = [partner_fields.get(col, [col])[0] for col in columns_f2]
    other_file_content_str = other_file_content_str.replace(first_line_f2, ','.join(mapped_columns_f2))

    logger.debug("Reading data into DataFrames")
    if enrollment_filename.endswith('.csv'):
        df_enrollment = pd.read_csv(io.StringIO(enrollment_file_content_str))
    elif enrollment_filename.endswith('.xlsx'):
        df_enrollment = pd.read_excel(io.BytesIO(enrollment_file_content))
    else:
        logger.error("Unsupported file type for enrollment file")
        raise HTTPException(status_code=400, detail="Unsupported file type for enrollment file")

    if other_filename.endswith('.csv'):
        df_other = pd.read_csv(io.StringIO(other_file_content_str))
    elif other_filename.endswith('.xlsx'):
        df_other = pd.read_excel(io.BytesIO(other_file_content))
    else:
        logger.error("Unsupported file type for other file")
        raise HTTPException(status_code=400, detail="Unsupported file type for other file")

    return df_enrollment, df_other

def cleanse_data(df_symetra, df_partner):
    """
    Cleanses the data by normalizing and formatting columns.

    Args:
        df_symetra (DataFrame): The Symetra DataFrame.
        df_partner (DataFrame): The partner DataFrame.

    Returns:
        tuple: Cleaned DataFrames for Symetra and partner data.
    """
    logger.debug("Cleansing data")
    if 'full name' in df_symetra.columns:
        df_symetra[['last name', 'first name']] = df_symetra['full name'].str.split(', ', expand=True)
    else:
        logger.error("The 'full name' column is not found in the enrollment DataFrame")
        raise HTTPException(status_code=400, detail="The 'full name' column is not found in the enrollment DataFrame")

    df_symetra = df_symetra.replace([pd.NA, np.nan, float('inf'), float('-inf')], None)
    df_partner = df_partner.replace([pd.NA, np.nan, float('inf'), float('-inf')], None)

    df_symetra['last name'] = df_symetra['last name'].str.lower()
    df_symetra['first name'] = df_symetra['first name'].str.lower()
    df_partner['last name'] = df_partner['last name'].str.lower()
    df_partner['first name'] = df_partner['first name'].str.lower()

    df_symetra['dob'] = pd.to_datetime(df_symetra['dob']).dt.strftime('%m/%d/%Y')
    df_partner['dob'] = pd.to_datetime(df_partner['dob']).dt.strftime('%m/%d/%Y')

    df_symetra['gender'] = df_symetra['gender'].apply(normalize_gender)
    df_partner['gender'] = df_partner['gender'].apply(normalize_gender)

    return df_symetra, df_partner

def validate_and_normalize_data(df_symetra, df_partner):
    """
    Validates and normalizes the data based on predefined rules.

    Args:
        df_symetra (DataFrame): The Symetra DataFrame.
        df_partner (DataFrame): The partner DataFrame.

    Returns:
        tuple: Validated and normalized DataFrames for Symetra and partner data.
    """
    logger.debug("Validating and normalizing data")
    for key, (column_name, column_type) in partner_fields.items():
        if column_type == "string":
            df_partner[column_name] = df_partner[column_name].apply(validate_and_normalize_string)
        elif column_type == "date":
            df_partner[column_name] = df_partner[column_name].apply(validate_and_normalize_date)
        elif column_type == "currency":
            df_partner[column_name] = df_partner[column_name].apply(normalize_and_validate_dollar_amount)
        elif column_type == "name":
            df_partner[column_name] = df_partner[column_name].apply(validate_and_normalize_names)

    for key, (column_name, column_type) in enrollment_fields.items():
        if column_type == "string":
            df_symetra[column_name] = df_symetra[column_name].apply(validate_and_normalize_string)
        elif column_type == "date":
            df_symetra[column_name] = df_symetra[column_name].apply(validate_and_normalize_date)
        elif column_type == "currency":
            df_symetra[column_name] = df_symetra[column_name].apply(normalize_and_validate_dollar_amount)
        elif column_type == "name":
            df_symetra[column_name] = df_symetra[column_name].apply(validate_and_normalize_names)

    return df_symetra, df_partner

def merge_dataframes(df_symetra, df_partner):
    """
    Merges the dataframes and identifies records unique to each file.

    Args:
        df_symetra (DataFrame): The Symetra DataFrame.
        df_partner (DataFrame): The partner DataFrame.

    Returns:
        tuple: Merged DataFrame and DataFrames for records unique to each file.
    """
    logger.debug("Merging dataframes")
    df_merged = df_symetra.merge(df_partner, on=base_matching_attribs, how='outer', indicator=True)
    df_merged = df_merged.replace([pd.NA, np.nan, float('inf'), float('-inf')], None)

    df_only_in_enrollment = df_merged[df_merged['_merge'] == 'left_only'][['first name', 'last name']]
    df_only_in_other = df_merged[df_merged['_merge'] == 'right_only'][['first name', 'last name']]

    df_merged = df_merged.rename(columns=lambda x: x.replace('_x', '_partner').replace('_y', '_symetra'))

    return df_merged, df_only_in_enrollment, df_only_in_other

def generate_response(df_merged, df_only_in_enrollment, df_only_in_other):
    """
    Generates the response by identifying changes.

    Args:
        df_merged (DataFrame): The merged DataFrame.
        df_only_in_enrollment (DataFrame): DataFrame for records only in the enrollment file.
        df_only_in_other (DataFrame): DataFrame for records only in the partner file.

    Returns:
        dict: The generated response.
    """
    logger.debug("Generating response")
    response = {'general': [], 'customer': []}

    for item in df_only_in_enrollment.to_dict(orient='records'):
        related_row = df_merged[
            (df_merged['first name'] == item['first name']) & (df_merged['last name'] == item['last name']) & (
                        df_merged['_merge'] == 'left_only')].to_dict(orient='records')[0]
        item.update(related_row)
        item['change'] = 'Partner Enrollment file - add'
        response['general'].append(item)

    for item in df_only_in_other.to_dict(orient='records'):
        related_row = df_merged[
            (df_merged['first name'] == item['first name']) & (df_merged['last name'] == item['last name']) & (
                        df_merged['_merge'] == 'right_only')].to_dict(orient='records')[0]
        item.update(related_row)
        item['change'] = 'Symetra Enrollment file - remove'
        response['general'].append(item)

    df_merged_base = df_merged[df_merged['_merge'] == 'both']
    conditions = [df_merged_base[f"{col}_partner"] != df_merged_base[f"{col}_symetra"] for col in extended_bases_attribs]
    df_base_diffs = df_merged_base[np.logical_or.reduce(conditions)]
    for item in df_base_diffs.to_dict(orient='records'):
        changes = []
        for col in extended_bases_attribs:
            if item[f"{col}_partner"] != item[f"{col}_symetra"]:
                changes.append(f"{col} changed from {item[f'{col}_partner']} to {item[f'{col}_symetra']}")
        item['change'] = '; '.join(changes)
        response['general'].append(item)

    for product in core_product_names:
        cols_to_check = [f"{product} {attrib}" for attrib in core_product_attribs]
        existing_cols_to_check = [col for col in cols_to_check if col in df_merged.columns]

        conditions = [df_merged[f"{col}_partner"] != df_merged[f"{col}_symetra"] for col in existing_cols_to_check]
        df_product_diffs = df_merged[np.logical_or.reduce(conditions)]

        for item in df_product_diffs.to_dict(orient='records'):
            changes = []
            for col in existing_cols_to_check:
                if item[f"{col}_partner"] != item[f"{col}_symetra"]:
                    changes.append(f"{col} changed from {item[f'{col}_partner']} to {item[f'{col}_symetra']}")
            item['change'] = '; '.join(changes)
            response['general'].append(item)

    return response

def consolidate_and_order_response(response, fixed_columns=None, match_patterns=None, drop_columns=None):
    """
    Consolidates and orders the response data.

    Args:
        response (dict): The response data.
        fixed_columns (list, optional): The fixed columns to appear first.
        match_patterns (list, optional): The regex patterns to match columns.
        drop_columns (list, optional): The columns to drop.

    Returns:
        dict: The consolidated and ordered response data.
    """
    logger.debug("Consolidating and ordering response")
    # Consolidate the response for only 1 first and last name
    consolidated_response = {}
    for item in response['general']:
        key = (item['first name'], item['last name'])
        if key not in consolidated_response:
            consolidated_response[key] = item
        else:
            consolidated_response[key]['change'] += '; ' + item['change']

    # Convert the dictionary back to a list
    response['general'] = list(consolidated_response.values())

    # Move the change column to show up after the last name column
    for item in response['general']:
        change_value = item.pop('change')
        last_name_index = list(item.keys()).index('last name')
        reordered_item = {k: item[k] for k in list(item.keys())[:last_name_index + 1]}
        reordered_item['change'] = change_value
        reordered_item.update({k: item[k] for k in list(item.keys())[last_name_index + 1:]})
        item.clear()
        item.update(reordered_item)

    # Drop specified columns
    if drop_columns:
        for item in response['general']:
            for col in drop_columns:
                item.pop(col, None)

    # Reorder columns based on the fixed columns, regex patterns, and alphabetical order for the rest
    if fixed_columns and match_patterns:
        for item in response['general']:
            matched_columns = []
            for pattern in match_patterns:
                regex = re.compile(pattern)
                matched_columns.extend([col for col in item.keys() if regex.match(col)])
            remaining_columns = sorted([col for col in item.keys() if col not in fixed_columns + matched_columns])
            final_column_order = fixed_columns + matched_columns + remaining_columns
            ordered_item = {col: item[col] for col in final_column_order if col in item}
            item.clear()
            item.update(ordered_item)

    return response

@router.post("/api/benefitscompare")
async def benefits_compare(
        request: Request,
        file1: UploadFile = File(...),
        file2: UploadFile = File(...)
):
    """
    API endpoint for comparing benefits data between two files.

    Args:
        request (Request): The request object.
        file1 (UploadFile): The first uploaded file.
        file2 (UploadFile): The second uploaded file.

    Returns:
        JSON: The comparison result as a JSON object.
    """
    try:
        form_data = await request.form()
        df_symetra, df_partner = await process_files(file1, file2)
        df_symetra, df_partner = cleanse_data(df_symetra, df_partner)

        if form_data['validateData'] == 'true' or form_data['normalizeData'] == 'true':
            df_symetra, df_partner = validate_and_normalize_data(df_symetra, df_partner)

        df_merged, df_only_in_symetra, df_only_in_partner = merge_dataframes(df_symetra, df_partner)

        response = {'general': [], 'customer': []}

        for item in df_only_in_symetra.to_dict(orient='records'):
            related_row = df_merged[
                (df_merged['first name'] == item['first name']) & (df_merged['last name'] == item['last name']) & (
                            df_merged['_merge'] == 'left_only')].to_dict(orient='records')[0]
            item.update(related_row)
            item['change'] = 'Symetra only entry - remove'
            response['general'].append(item)

        for item in df_only_in_partner.to_dict(orient='records'):
            related_row = df_merged[
                (df_merged['first name'] == item['first name']) & (df_merged['last name'] == item['last name']) & (
                            df_merged['_merge'] == 'right_only')].to_dict(orient='records')[0]
            item.update(related_row)
            item['change'] = 'Partner only entry - add'
            response['general'].append(item)

        # This finds the differences in the base attributes
        df_merged_base = df_symetra.merge(df_partner, on=base_matching_attribs, suffixes=('_enrollment', '_other'))
        conditions = [df_merged_base[f"{col}_enrollment"] != df_merged_base[f"{col}_other"] for col in
                      extended_bases_attribs]
        df_base_diffs = df_merged_base[np.logical_or.reduce(conditions)]

        for item in df_base_diffs.to_dict(orient='records'):
            changes = []
            for col in extended_bases_attribs:
                if item[f"{col}_enrollment"] != item[f"{col}_other"]:
                    changes.append(f"{col} changed from {item[f'{col}_enrollment']} to {item[f'{col}_other']}")
            item['change'] = '; '.join(changes)
            response['general'].append(item)

        # this produces the list of things different between the two files for products
        for product in core_product_names:
            cols_to_check = [f"{product} {attrib}" for attrib in core_product_attribs]
            existing_cols_to_check = [col for col in cols_to_check if
                                      col in df_symetra.columns and col in df_partner.columns]

            df_merged = df_symetra.merge(df_partner, on=base_matching_attribs, suffixes=('_enrollment', '_other'))

            conditions = [df_merged[f"{col}_enrollment"] != df_merged[f"{col}_other"] for col in existing_cols_to_check]
            df_product_diffs = df_merged[np.logical_or.reduce(conditions)]

            # Iterate over the df_product_diffs and add to the response message
            for item in df_product_diffs.to_dict(orient='records'):
                changes = []
                for col in existing_cols_to_check:
                    if item[f"{col}_enrollment"] != item[f"{col}_other"]:
                        changes.append(f"{col} changed from {item[f'{col}_enrollment']} to {item[f'{col}_other']}")
                item['change'] = '; '.join(changes)
                response['general'].append(item)
        # TODO - End the move to the new function

        response = consolidate_and_order_response(response, sort_fixed_columns, sort_match_columns, drop_columns)

        return json.dumps(response)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")