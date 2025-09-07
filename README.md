# Lottery Analysis (Google Sheets + GitHub Actions + Streamlit)

This starter lets you:
- Backfill ~300 days of results (Miền Bắc) into Google Sheets
- Auto-update daily via GitHub Actions
- View analysis (khan >=7, frequency windows, Method 1 & 2) on a Streamlit web app

> Legal note: This is *statistical analysis of published lottery results*, **not** a betting tool.

## What you'll need
1. A Google account
2. A GitHub account
3. (Optional) A Streamlit Cloud account (sign in with GitHub)

## Quick steps
1. Create a Google Sheet (empty) and note its **Spreadsheet ID** (the long string in the URL).
2. Create a Google Cloud **Service Account**, enable **Google Sheets API** and **Google Drive API**, and download the JSON key.
3. Share your Sheet with the service account email (Editor permission).
4. Create a new GitHub repo, upload all files from this starter.
5. Add GitHub repository secrets:
   - `GCP_SERVICE_ACCOUNT_JSON` → paste the full JSON key
   - `SHEET_ID` → your spreadsheet ID
   - (Optional) `SHEET_NAME` → name of spreadsheet (if you prefer name-based open)
6. Trigger a **manual backfill** in GitHub Actions (workflow: *Backfill 300 days*).
7. Deploy `streamlit_app.py` on Streamlit Cloud (connect repo).

## Data model (Sheets)
- Worksheet **raw_daily_lo2d**: one row per day, 27 (or more) two-digit numbers as columns
  - columns: `date,n1,n2,...,n27`
- Worksheet **daily_counts**: exploded rows with `date,number,count`
- Worksheet **analysis_today**: summary per number 00–99 with gaps, frequencies, and scores

> If raw parsing fails on any date, you can manually paste numbers into `raw_daily_lo2d` temporarily.

## Run locally (optional)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GCP_SERVICE_ACCOUNT_JSON='{"type":"service_account", ... }'
export SHEET_ID='your_google_sheet_id'
python pipeline.py --backfill 300
python pipeline.py --update-today
streamlit run streamlit_app.py
```

## Timezone
- GitHub Actions is UTC. For Viet Nam (UTC+7), a 18:40 local run ≈ 11:40 UTC. Adjust in `.github/workflows/update.yml`.

## Disclaimer
Scrapers may break if source sites change HTML. You can always fall back to manual paste for problematic dates.
