 

import requests 

from datetime import date, timedelta 

from bs4 import BeautifulSoup 

 

 

def fetch_for_date(d: date): 

    """ 

    Lấy kết quả xổ số miền Bắc cho 1 ngày cụ thể. 

    Ưu tiên lấy từ ketqua.net, nếu lỗi sẽ tự fallback sang xskt.net. 

    Trả về list gồm 27 số (theo thứ tự các giải). 

    """ 

    date_str = d.strftime("%d-%m-%Y") 

 

    # Danh sách các nguồn dự phòng 

    urls = [ 

        f"https://ketqua.net/xo-so-mien-bac-ngay-{date_str}", 

        f"https://xskt.net/xo-so-mien-bac-ngay-{date_str}", 

    ] 

 

    for url in urls: 

        print(f"🔹 Fetching: {url}") 

        try: 

            r = requests.get(url, timeout=15) 

            r.raise_for_status() 

            html = r.text 

 

            soup = BeautifulSoup(html, "html.parser") 

 

            # Tìm tất cả các số trong bảng kết quả 

            numbers = [span.text.strip() for span in soup.select("td span, div span") if span.text.strip().isdigit()] 

 

            # Lọc bỏ số trùng và chỉ lấy 27 số đầu tiên 

            unique_numbers = [] 

            for n in numbers: 

                if n not in unique_numbers: 

                    unique_numbers.append(n) 

            result = unique_numbers[:27] 

 

            if len(result) >= 10: 

                print(f"✅ Lấy dữ liệu ngày {d} thành công ({len(result)} số).") 

                return result 

            else: 

                print(f"⚠️ Số lượng kết quả ít ({len(result)}), thử nguồn khác...") 

 

        except Exception as e: 

            print(f"⚠️ Lỗi khi lấy từ {url}: {e}") 

 

    print(f"❌ Không lấy được dữ liệu ngày {d}.") 

    return [] 

 

 

def fetch_range(days: int): 

    """ 

    Lấy dữ liệu nhiều ngày gần nhất. 

    Trả về dict: { 'YYYY-MM-DD': [list 27 số], ... } 

    """ 

    results = {} 

    today = date.today() 

    for i in range(days): 

        d = today - timedelta(days=i) 

        arr = fetch_for_date(d) 

        results[d.isoformat()] = arr 

    return results 

 

 

if __name__ == "__main__": 

    # Test riêng file này 

    print("🧪 Đang test fetch cho hôm nay...") 

    today = date.today() 

    data = fetch_for_date(today) 

    print(f"Kết quả: {data}") 
