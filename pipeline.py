from __future__ import annotations
import os
import argparse
from datetime import date
import pandas as pd

from gsheets_utils import open_spreadsheet, ensure_worksheet, write_dataframe, read_dataframe
from fetch_xsmb import fetch_range, fetch_for_date
from analysis import explode_raw_daily_lo2d, make_full_calendar_counts, make_analysis_table

RAW_WS = 'raw_daily_lo2d'
COUNTS_WS = 'daily_counts'
ANALYSIS_WS = 'analysis_today'

def _append_or_update_raw(ws, new_df: pd.DataFrame):
    # Read current, append unique dates
    cur = read_dataframe(ws)
    if cur.empty:
        # ép date về dạng string trước khi ghi
        new_df['date'] = pd.to_datetime(new_df['date']).dt.strftime("%Y-%m-%d")
        write_dataframe(ws, new_df)
        return

    merged = pd.concat([cur, new_df], ignore_index=True)

    # Ép toàn bộ cột date về string YYYY-MM-DD
    merged['date'] = pd.to_datetime(merged['date']).dt.strftime("%Y-%m-%d")

    # Keep latest for each date
    merged = merged.sort_values('date').drop_duplicates(subset=['date'], keep='last')
    write_dataframe(ws, merged)

def backfill(days: int):
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
    # also refresh counts + analysis
    refresh_analysis()

def update_today():
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
    ss = open_spreadsheet()
    ws_raw = ensure_worksheet(ss, RAW_WS)
    ws_counts = ensure_worksheet(ss, COUNTS_WS)
    ws_ana = ensure_worksheet(ss, ANALYSIS_WS)

    raw_df = read_dataframe(ws_raw)
    if raw_df.empty:
        print('No raw data yet.')
        return

    # Ép date về kiểu datetime cho phân tích
    raw_df['date'] = pd.to_datetime(raw_df['date']).dt.date
    start_date = raw_df['date'].min()
    end_date = raw_df['date'].max()

    counts = explode_raw_daily_lo2d(raw_df)
    full = make_full_calendar_counts(counts, start_date, end_date)
    write_dataframe(ws_counts, full)

    analysis = make_analysis_table(full, end_date)
    write_dataframe(ws_ana, analysis)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backfill', type=int, help='Fetch N days history and rebuild analysis.')
    parser.add_argument('--update-today', action='store_true', help='Fetch today and update analysis.')
    args = parser.parse_args()

    if args.backfill:
backfill(args.backfill)
    elif args.update_today:
        update_today()
    else:
        print('Nothing to do. Use --backfill N or --update-today.')
