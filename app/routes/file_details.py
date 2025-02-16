from fastapi import APIRouter, File, UploadFile, HTTPException, Request
import pandas as pd
import io
import numpy as np

router = APIRouter()

@router.post("/api/getfiledetails")
async def file_stats(request: Request, file: UploadFile = File(...)):
    try:
        file1_content = await file.read()
        if file.filename.endswith('.csv'):
            df_file = pd.read_csv(io.StringIO(file1_content.decode('utf-8')))
        elif file.filename.endswith('.xlsx'):
            df_file = pd.read_excel(io.BytesIO(file1_content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type for file")

        file_size = len(file1_content)
        num_rows = df_file.shape[0]
        num_columns = df_file.shape[1]

        response = {
            'file_name': file.filename,
            'file_size': file_size,
            'num_rows': num_rows,
            'num_columns': num_columns,
            'columns': df_file.columns.to_list()
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")