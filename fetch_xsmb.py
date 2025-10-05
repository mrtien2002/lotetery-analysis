import requests 

import datetime 

import pandas as pd 

 

# URL nguồn dữ liệu xổ số miền Bắc 

BASE_URL = "https://api.xoso.me/app/json-kq-mienbac" 

 

def fetch_for_date(d: datetime.date): 

    """Lấy kết quả cho 1 ngày""" 

    date_str = d.strftime("%d-%m-%Y") 

    url = f"{BASE_URL}?date={date_str}" 

    print(f"🔹 Fetching {url}") 

    r = requests.get(url) 

    if r.status_code != 200: 

        raise Exception(f"❌ Không thể tải dữ liệu ngày {date_str}: {r.status_code}") 

 

    data = r.json() 

    if "data" not in data or "MB" not in data["data"]: 

        raise Exception(f"❌ Dữ liệu không hợp lệ cho ngày {date_str}") 

 

    prizes = data["data"]["MB"]["prizes"] 

    all_nums = [] 

    for p in prizes.values(): 

        for num in p: 

            all_nums.append(str(num)[-2:].zfill(2)) 

    return all_nums 

 

def fetch_range(days: int): 

    """Lấy dữ liệu N ngày gần nhất""" 

    today = datetime.date.today() 

    results = {} 

    for i in range(days): 

        d = today - datetime.timedelta(days=i) 

        try: 

            results[d.isoformat()] = fetch_for_date(d) 

        except Exception as e: 

            print(f"⚠️ Bỏ qua {d}: {e}") 

    return results 

 

if __name__ == "__main__": 

    # Test chạy trực tiếp 

    print(fetch_for_date(datetime.date.today())) 
