 

import requests 

from bs4 import BeautifulSoup 

from datetime import date 

 

HEADERS = { 

    'User-Agent': 'Mozilla/5.0' 

} 

 

ORDER = ["ĐB", "G1", "G2", "G3", "G4", "G5", "G6", "G7"] 

COUNTS = [1, 1, 2, 6, 4, 6, 3, 4] 

 

def fetch_xskt(d: date) -> list[str]: 

    url = f"https://xskt.net/so-ket-qua-300-ngay?ngay={d.strftime('%d-%m-%Y')}" 

    r = requests.get(url, headers=HEADERS, timeout=30) 

    r.raise_for_status() 

    soup = BeautifulSoup(r.text, "lxml") 

    text = soup.get_text("\n", strip=True) 

 

    results = [] 

    for label, count in zip(ORDER, COUNTS): 

        pattern = rf"{label}\s+([\d\s]+)" 

        m = re.search(pattern, text) 

        if not m: 

            results.extend([""] * count) 

            continue 

        line = m.group(1).strip() 

        nums = re.findall(r"\d+", line) 

        nums = [n[-2:].zfill(2) for n in nums] 

        results.extend(nums[:count] + [""] * max(0, count - len(nums))) 

    return results 

 

if __name__ == "__main__": 

    for d in [date(2025, 9, 8), date(2025, 9, 9)]: 

        try: 

            arr = fetch_xskt(d) 

            print(f"{d} ({len(arr)} số): {arr}") 

        except Exception as e: 

            print(f"Lỗi {d}: {e}") 
