from __future__ import annotations
import re
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari'
}

def extract_two_digits_all(text: str):
    # find all numbers with 2+ digits, then take last two digits of each
    nums = re.findall(r'\d{2,}', text)
    return [f"{int(n[-2:]):02d}" for n in nums]

def fetch_minhngoc(d: date):
    # Example URL pattern: https://www.minhngoc.net.vn/ket-qua-xo-so/mien-bac/01-09-2025.html
    url = f"https://www.minhngoc.net.vn/ket-qua-xo-so/mien-bac/{d.strftime('%d-%m-%Y')}.html"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    # Try to target result area; fallback to whole page text
    container = soup.find(id='kqmb') or soup
    text = container.get_text(' ', strip=True)
    arr = extract_two_digits_all(text)
    # Heuristic: return top ~27–35 last-two-digit numbers of the day
    # Deduplicate while preserving order
    seen = []
    for v in arr:
        if v not in seen:
            seen.append(v)
    # keep first 30 as a safe cap
    return seen[:30]

def fetch_xskt(d: date):
    # Fallback parser for xskt-like layout (best-effort, may need adjustments)
    url = f"https://xskt.com.vn/ket-qua-xo-so/mien-bac/{d.strftime('%d-%m-%Y')}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.get_text(' ', strip=True)
    arr = extract_two_digits_all(text)
    seen = []
    for v in arr:
        if v not in seen:
            seen.append(v)
    return seen[:30]

def fetch_for_date(d: date):
    # Try minhngoc first, then xskt
    try:
        return fetch_minhngoc(d)
    except Exception:
        return fetch_xskt(d)

def fetch_range(days: int, end_date: date | None = None):
    if end_date is None:
        end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    results = {}
    for i in range(days):
        d = start_date + timedelta(days=i)
        try:
            arr = fetch_for_date(d)
            results[d.isoformat()] = arr
        except Exception as e:
            results[d.isoformat()] = []  # leave blank; can be manually filled later
    return results
