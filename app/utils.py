import re
import datetime

def normalize_gender(gender: str) -> str:
    if gender is None or gender == "":
        return "null"
    normalized_gender = gender.strip().lower()
    gender_map = {
        "male": ["male", "m", "man", "boy"],
        "female": ["female", "f", "woman", "girl"],
        "other": ["other", "non-binary", "nonbinary", "nb", "genderqueer", "genderfluid"]
    }
    for standard_gender, variations in gender_map.items():
        if normalized_gender in variations:
            return standard_gender
    return "other"

def normalize_phone_number(phone_number: str) -> str:
    normalized_number = re.sub(r'\D', '', phone_number)
    return normalized_number.zfill(11)[:11]

def normalize_and_validate_dollar_amount(amount: str) -> str:
    if amount is None or amount == "":
        return "null"
    amount_str = str(amount)
    normalized_amount = re.sub(r'[^\d.]', '', amount_str)
    if normalized_amount == "":
        return "null"
    try:
        float_amount = float(normalized_amount)
    except ValueError:
        raise ValueError(f"Invalid dollar amount")
    return f"{float_amount:.2f}"

def validate_and_normalize_date(date_str: str) -> str:
    if date_str is None or date_str == "":
        return "null"
    date_formats = ["%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
    for date_format in date_formats:
        try:
            date_obj = datetime.datetime.strptime(date_str, date_format)
            return date_obj.strftime("%m/%d/%Y")
        except ValueError:
            continue
    raise ValueError("Invalid date format")

def normalize_email(email: str) -> str:
    return email.strip().lower()

def validate_and_normalize_names(value: str) -> str:
    if not isinstance(value, str) or value is None or value == "":
        return "null"
    normalized_name = re.sub(r'-', '', value)
    return normalized_name.strip().lower()

def validate_and_normalize_string(value: str) -> str:
    if not isinstance(value, str) or value is None or value == "":
        return "null"
    normalized_value = value.strip().lower()
    return normalized_value
