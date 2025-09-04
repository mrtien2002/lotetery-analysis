import os
import pandas as pd
from datetime import datetime, date
import gspread
from google.oauth2.service_account import Credentials

# ==== CONFIG ====
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # ID Google Sheet
RAW_SHEET_NAME = "raw"  # tên sheet chứa dữ liệu gốc

# ==== GOOGLE SHEETS ====
def _get_ws(sheet_name: str):
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)

# ==== CLEAN DATE ====
def _clean_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Ép cột date về datetime.date"""
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    return df

# ==== APPEND OR UPDATE RAW ====
def _append_or_update_raw(ws, new_df: pd.DataFrame):
    """Ghi dữ liệu mới vào sheet raw, update theo cột date"""
    # Lấy dữ liệu cũ
    old_values = ws.get_all_records()
    old_df = pd.DataFrame(old_values) if old_values else pd.DataFrame(columns=["date", "result"])

    # Ép date
    if not old_df.empty:
        old_df = _clean_date_column(old_df)
    new_df = _clean_date_column(new_df)

    # Gộp
    merged = pd.concat([old_df, new_df], ignore_index=True)
    merged = merged.sort_values("date").drop_duplicates(subset=["date"], keep="last")

    # Convert date -> string ISO
    merged["date"] = merged["date"].apply(lambda x: x.strftime("%Y-%m-%d") if isinstance(x, date) else x)

    # Clear sheet & ghi lại
    ws.clear()
    ws.update([merged.columns.values.tolist()] + merged.values.tolist())
    print("✅ Raw data updated!")

# ==== LẤY DỮ LIỆU MỚI (ví dụ fake) ====
def _fetch_today() -> pd.DataFrame:
    """Hàm này bạn thay bằng crawler thực tế"""
    today = datetime.today().date()
    dummy = {"date": [today], "result": ["12345"]}
    return pd.DataFrame(dummy)

# ==== MAIN ====
def update_today():
    ws_raw = _get_ws(RAW_SHEET_NAME)
    df = _fetch_today()
    _append_or_update_raw(ws_raw, df)

if __name__ == "__main__":
    import sys
    if "--update-today" in sys.argv:
        update_today()
