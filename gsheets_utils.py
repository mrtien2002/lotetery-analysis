import os
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe, get_as_dataframe

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

def _get_sa_info():
    # Prefer env var; else service_account.json file in project root
    json_str = os.environ.get('GCP_SERVICE_ACCOUNT_JSON')
    if json_str:
        return json.loads(json_str)
    if os.path.exists('service_account.json'):
        with open('service_account.json','r',encoding='utf-8') as f:
            return json.load(f)
    raise RuntimeError('Service account JSON not found. Set env GCP_SERVICE_ACCOUNT_JSON or place service_account.json in project root.')

def get_client():
    sa_info = _get_sa_info()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(sa_info, SCOPES)
    return gspread.authorize(creds)

def open_spreadsheet():
    gc = get_client()
    sheet_id = os.environ.get('SHEET_ID')
    sheet_name = os.environ.get('SHEET_NAME')

    if sheet_id:
        return gc.open_by_key(sheet_id)
    if sheet_name:
        return gc.open(sheet_name)
    raise RuntimeError('Provide SHEET_ID or SHEET_NAME as environment variable.')

def ensure_worksheet(spreadsheet, title, rows=1000, cols=40):
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows=str(rows), cols=str(cols))
    return ws

def write_dataframe(ws, df: pd.DataFrame, include_index=False, resize=True):
    if resize:
        ws.resize(rows=len(df)+1, cols=len(df.columns)+1)
    set_with_dataframe(ws, df, include_index=include_index, resize=False)

def read_dataframe(ws) -> pd.DataFrame:
    df = get_as_dataframe(ws, evaluate_formulas=True, header=0)
    # Drop all-empty rows
    if df is None:
        return pd.DataFrame()
    df = df.dropna(how='all')
    # Normalize date column if present
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.date
    return df
