import re 

import requests 

from bs4 import BeautifulSoup 

from datetime import date 

 

HEADERS = { 

    'User-Agent': 'Mozilla/5.0' 

} 

 

# Thứ tự các giải và số lượng giải 

PRIZE_ORDER = [ 

    ("Giải ĐB", 1), 

    ("Giải nhất", 1), 

    ("Giải nhì", 2), 

    ("Giải ba", 6), 

    ("Giải tư", 4), 

    ("Giải năm", 6), 

    ("Giải sáu", 3), 

    ("Giải bảy", 4), 

] 

 

def fetch_minhngoc(d: date): 

    url = f"https://www.minhngoc.net.vn/ket-qua-xo-so/mien-bac/{d.strftime('%d-%m-%Y')}.html" 

    r = requests.get(url, headers=HEADERS, timeout=30) 

    r.raise_for_status() 

    soup = BeautifulSoup(r.text, "lxml") 

 

    container = soup.find(id="kqmb") 

    if not container: 

        raise RuntimeError("Không tìm thấy khung kết quả") 

 

    results = [] 

    for label, count in PRIZE_ORDER: 

        node = container.find(string=re.compile(label, re.I)) 

        numbers = [] 

        if node: 

            sib = node.parent.find_next_sibling() 

            while sib and len(numbers) < count: 

                text = sib.get_text(strip=True) 

                if re.fullmatch(r"\d+", text): 

                    numbers.append(text[-2:]) 

                sib = sib.find_next_sibling() 

        # nếu thiếu thì pad rỗng 

        numbers += [""] * (count - len(numbers)) 

        results.extend(numbers[:count]) 

 

    return results 

 

if __name__ == "__main__": 

    for d in [date(2025, 9, 6), date(2025, 9, 7)]: 

        try: 

            nums = fetch_minhngoc(d) 

            print(f"{d} -> {len(nums)} số: {nums}") 

        except Exception as e: 

            print(f"{d} lỗi: {e}") 
