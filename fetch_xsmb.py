from __future__ import annotations 

import re 

from datetime import date, timedelta 

import requests 

from bs4 import BeautifulSoup 

 

HEADERS = { 

    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari' 

} 

 

def extract_two_digits_all(text: str): 

    # tìm tất cả số có >= 2 chữ số, lấy 2 số cuối của mỗi số 

    nums = re.findall(r'\d{2,}', text) 

    return [f"{int(n[-2:]):02d}" for n in nums] 

 

def normalize_to_27(arr: list[str]) -> list[str]: 

    """ 

    Chuẩn hóa kết quả về đúng 27 số (theo lô 2 chữ số miền Bắc). 

    - Nếu thừa (>27): lấy 27 số đầu tiên. 

    - Nếu thiếu (<27): padding thêm '' cho đủ 27. 

    """ 

    if len(arr) >= 27: 

        return arr[:27] 

    else: 

        return arr + [''] * (27 - len(arr)) 

 

def fetch_minhngoc(d: date) -> list[str]: 

    url = f"https://www.minhngoc.net.vn/ket-qua-xo-so/mien-bac/{d.strftime('%d-%m-%Y')}.html" 

    r = requests.get(url, headers=HEADERS, timeout=30) 

    r.raise_for_status() 

    soup = BeautifulSoup(r.text, 'lxml') 

    container = soup.find(id='kqmb') or soup 

    text = container.get_text(' ', strip=True) 

    arr = extract_two_digits_all(text) 

 

    # Loại bỏ trùng lặp, giữ thứ tự 

    seen = [] 

    for v in arr: 

        if v not in seen: 

            seen.append(v) 

 

    return normalize_to_27(seen) 

 

def fetch_xskt(d: date) -> list[str]: 

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

 

    return normalize_to_27(seen) 

 

def fetch_for_date(d: date) -> list[str]: 

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

            results[d.isoformat()] = []  # lỗi thì để trống 

    return results 