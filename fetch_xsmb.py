import requests 

from datetime import date, timedelta 

from bs4 import BeautifulSoup 

 

# Danh sách các domain dự phòng 

DOMAINS = [ 

    "https://ketqua.net", 

    "https://xoso.me", 

    "https://www.minhngoc.net.vn" 

] 

 

def _fetch_from_domain(domain: str, d: date): 

    """Thử lấy dữ liệu từ 1 domain cụ thể""" 

    date_str = d.strftime("%d-%m-%Y") 

    url = f"{domain}/xo-so-mien-bac-ngay-{date_str}" 

    print(f"🔹 Fetching: {url}") 

    try: 

        r = requests.get(url, timeout=10) 

        r.raise_for_status() 

    except Exception as e: 

        print(f"⚠️ Không truy cập được {domain}: {e}") 

        return None 

 

    # Phân tích HTML 

    soup = BeautifulSoup(r.text, "html.parser") 

    text = soup.get_text(" ", strip=True) 

    numbers = [] 

 

    for part in text.split(): 

        if part.isdigit() and len(part) in (2, 5): 

            n2 = part[-2:] 

            if n2.isdigit(): 

                numbers.append(n2) 

 

    if len(numbers) >= 27: 

        return numbers[-27:]  # Lấy 27 số cuối 

    return None 

 

 

def fetch_for_date(d: date): 

    """Lấy kết quả cho 1 ngày (tự thử nhiều domain nếu lỗi)""" 

    for domain in DOMAINS: 

        result = _fetch_from_domain(domain, d) 

        if result: 

            print(f"✅ Lấy thành công từ {domain}: {len(result)} số.") 

            return result 

    raise RuntimeError(f"❌ Không thể lấy dữ liệu ngày {d.strftime('%d-%m-%Y')} từ bất kỳ domain nào.") 

 

 

def fetch_range(days: int): 

    """Lấy kết quả trong N ngày gần nhất""" 

    results = {} 

    today = date.today() 

    for i in range(days): 

        d = today - timedelta(days=i) 

        try: 

            results[d.isoformat()] = fetch_for_date(d) 

        except Exception as e: 

            print(f"⚠️ Bỏ qua {d}: {e}") 

    return results 
