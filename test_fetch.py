from datetime import date 

from fetch_xsmb import fetch_for_date, fetch_minhngoc, fetch_xskt 

 

today = date(2025, 9, 7) 

 

try: 

    result = fetch_minhngoc(today) 

    print("✅ Lấy từ Minh Ngọc:", result) 

except Exception as e: 

    print("❌ Minh Ngọc lỗi:", e) 

    result = fetch_xskt(today) 

    print("👉 Fallback sang XSKT:", result) 
