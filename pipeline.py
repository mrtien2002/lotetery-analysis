from __future__ import annotations
import os
import argparse
from datetime import date, datetime
import pandas as pd

from gsheets_utils import open_spreadsheet, ensure_worksheet, write_dataframe, read_dataframe
from fetch_xsmb import fetch_range, fetch_for_date
from analysis import explode_raw_daily_lo2d, make_full_calendar_counts, make_analysis_table

RAW_WS = 'raw_daily_lo2d'
COUNTS_WS = 'daily_counts'
ANALYSIS_WS = 'analysis_today'

def _append_or_update_raw(ws, new_df: pd.DataFrame):
    """Thêm hoặc cập nhật dữ liệu vào worksheet RAW."""
    cur = read_dataframe(ws)

    # Ép date về datetime.date
    if not cur.empty:
        cur['date'] = pd.to_datetime(cur['date'], errors="coerce").dt.date
    new_df['date'] = pd.to_datetime(new_df['date'], errors="coerce").dt.date

    if cur.empty:
        write_dataframe(ws, new_df)
        return

    merged = pd.concat([cur, new_df], ignore_index=True)
    # Sắp xếp + bỏ trùng, giữ bản ghi mới nhất
    merged = merged.sort_values('date').drop_duplicates(subset=['date'], keep='last')
    write_dataframe(ws, merged)

def backfill(days: int):
    """Lấy dữ liệu N ngày gần nhất và rebuild phân tích."""
    ss = open_spreadsheet()
    ws_raw = ensure_worksheet(ss, RAW_WS)
    print(f"Fetching last {days} days...")
    results = fetch_range(days)
    rows = []
    for d_iso, arr in results.items():
        row = {'date': d_iso}
        for i, v in enumerate(arr, start=1):
            row[f'n{i}'] = v
        rows.append(row)
    df = pd.DataFrame(rows)
    _append_or_update_raw(ws_raw, df)
    refresh_analysis()

def update_today():
    """Lấy kết quả hôm nay và cập nhật phân tích."""
    ss = open_spreadsheet()
    ws_raw = ensure_worksheet(ss, RAW_WS)
    today = date.today().isoformat()
    arr = fetch_for_date(date.today())
    row = {'date': today}
    for i, v in enumerate(arr, start=1):
        row[f'n{i}'] = v
    df = pd.DataFrame([row])
    _append_or_update_raw(ws_raw, df)
    refresh_analysis()

def refresh_analysis():
    """Tạo bảng đếm & bảng phân tích từ dữ liệu RAW."""
    ss = open_spreadsheet()
    ws_raw = ensure_worksheet(ss, RAW_WS)
    ws_counts = ensure_worksheet(ss, COUNTS_WS)
    ws_ana = ensure_worksheet(ss, ANALYSIS_WS)

    raw_df = read_dataframe(ws_raw)
    if raw_df.empty:
        print("No raw data yet.")
        return

    # Chuẩn hóa date
    raw_df['date'] = pd.to_datetime(raw_df['date'], errors="coerce").dt.date
    start_date = raw_df['date'].min()
    end_date = raw_df['date'].max()

    counts = explode_raw_daily_lo2d(raw_df)
    full = make_full_calendar_counts(counts, start_date, end_date)
    write_dataframe(ws_counts, full)

    analysis = make_analysis_table(full, end_date)
    write_dataframe(ws_ana, analysis)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backfill", type=int, help="Fetch N days history and rebuild analysis.")
    parser.add_argument("--update-today", action="store_true", help="Fetch today and update analysis.")
    args = parser.parse_args()

    if args.backfill:
        backfill(args.backfill)
    elif args.update_today:
        update_today()
    else:
        print("Nothing to do. Use --backfill N or --update-today.")
