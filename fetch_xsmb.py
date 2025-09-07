import requests
from datetime import date, timedelta

API_URL = "https://api.xoso.me/smb"  # placeholder, cần chỉnh nếu API khác

def fetch_for_date(d: date):
    resp = requests.get(f"{API_URL}?date={d.isoformat()}")
    data = resp.json()
    return data.get("numbers", [])

def fetch_range(days: int):
    results = {}
    today = date.today()
    for i in range(days):
        d = today - timedelta(days=i)
        try:
            arr = fetch_for_date(d)
            results[d.isoformat()] = arr
        except Exception as e:
            print(f"Failed fetch {d}: {e}")
    return results
