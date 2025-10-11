from datetime import date, timedelta 

import requests 

from bs4 import BeautifulSoup 

 

DOMAINS = [ 

    "https://www.minhngoc.net.vn", 

    "https://xoso.me", 

    "https://ketqua.net" 

] 

 

def fetch_from_domain(domain: str, d: date): 

    url = f"{domain}/xo-so-mien-bac-ngay-{d.strftime('%d-%m-%Y')}" 

    print(f"🔹 Fetching: {url}") 

    try: 

        r = requests.get(url, timeout=10) 

        r.raise_for_status() 

    except Exception as e: 

        print(f"⚠️ Không truy cập được {domain}: {e}") 

        return None 

    soup = BeautifulSoup(r.text, "html.parser") 

    nums = [] 

    # Tìm các thẻ td hoặc span hoặc div chứa kết quả 

    for tag in soup.find_all(["td","span","div"]): 

        text = tag.get_text(strip=True) 

        if text.isdigit() and len(text) >= 2: 

            nums.append(text[-2:])  # lấy 2 số cuối 

    if len(nums) >= 27: 

        print(f"✅ Lấy được {len(nums)} số từ {domain}") 

        return nums[:27] 

    print(f"⚠️ Thiếu số ({len(nums)} số) từ {domain}") 

    return None 

 

def fetch_for_date(d: date): 

    for domain in DOMAINS: 

        arr = fetch_from_domain(domain, d) 

        if arr: 

            return arr 

    return None  # không lấy được 

 

def fetch_range(days: int): 

    results = {} 

    today = date.today() 

    for i in range(days): 

        d = today - timedelta(days=i) 

        arr = fetch_for_date(d) 

        if arr: 

            results[d.isoformat()] = arr 

        else: 

            print(f"⚠️ Bỏ qua ngày {d.strftime('%d-%m-%Y')} vì không lấy được kết quả") 

    return results 
