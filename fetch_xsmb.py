import requests 

from bs4 import BeautifulSoup 

from datetime import date, timedelta 

import re 

 

HEADERS = { 

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 

                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" 

} 

 

def extract_two_digits(text: str): 

    """Trích xuất 27 số cuối 2 chữ số từ văn bản""" 

    nums = re.findall(r'\d{2,}', text) 

    # Lấy 2 số cuối cùng của từng chuỗi 

    nums = [n[-2:] for n in nums] 

    # Giữ thứ tự, loại bỏ trùng 

    seen = [] 

    for n in nums: 

        if n not in seen: 

            seen.append(n) 

    return seen[-27:]  # chỉ lấy 27 số cuối (chuẩn của miền Bắc) 

 

def fetch_ketqua(d: date): 

    """Lấy kết quả từ trang ketqua.net""" 

    url = f"https://ketqua.net/xo-so-mien-bac-ngay-{d.strftime('%d-%m-%Y')}" 

    print(f"🔹 Fetching: {url}") 

    r = requests.get(url, headers=HEADERS, timeout=20) 

    r.raise_for_status() 

    soup = BeautifulSoup(r.text, "html.parser") 

 

    # Tìm bảng kết quả 

    result_table = soup.find("table", {"id": "result_tab_mb"}) 

    if not result_table: 

        raise ValueError("❌ Không tìm thấy bảng kết quả trên trang ketqua.net") 

 

    text = result_table.get_text(" ", strip=True) 

    numbers = extract_two_digits(text) 

    return numbers 

 

def fetch_for_date(d: date): 

    """Lấy kết quả 1 ngày""" 

    try: 

        return fetch_ketqua(d) 

    except Exception as e: 

        print(f"⚠️ Lỗi khi lấy dữ liệu ngày {d}: {e}") 

        return [] 

 

def fetch_range(days: int, end_date: date | None = None): 

    """Lấy kết quả trong nhiều ngày""" 

    if end_date is None: 

        end_date = date.today() 

    start_date = end_date - timedelta(days=days - 1) 

    results = {} 

    for i in range(days): 

        d = start_date + timedelta(days=i) 

        results[d.isoformat()] = fetch_for_date(d) 

    return results 
