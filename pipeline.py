import sys 

import subprocess 

from datetime import date 

import pandas as pd 

 

from fetch_xsmb import fetch_for_date, fetch_range 

# Bạn nhớ import các hàm từ các file khác (analysis, etc.) 

 

# (Giả định bạn có các file analyze_excel.py, analysis.py, analysis_evolution.py, predict_xien.py) 

 

def run(cmd): 

    print(">", " ".join(cmd)) 

    r = subprocess.run(cmd, shell=False) 

    if r.returncode != 0: 

        raise SystemExit(f"Lỗi khi chạy {' '.join(cmd)}") 

 

def update_today(): 

    # Trước hết thử fetch kết quả thật 

    arr = fetch_for_date(date.today()) 

    if arr is None: 

        print(f"⚠️ Không có kết quả web cho ngày {date.today().strftime('%d-%m-%Y')}. Dừng cập nhật hôm nay.") 

        sys.exit(0) 

 

    # Nếu có arr, tiếp tục các bước phân tích, ghi dữ liệu 

    # Ví dụ: 

    run([sys.executable, "analyze_excel.py"]) 

    run([sys.executable, "analysis.py"]) 

    run([sys.executable, "analysis_evolution.py"]) 

    run([sys.executable, "predict_xien.py"]) 

    print("✅ Cập nhật hôm nay hoàn tất.") 

 

def backfill(days: int): 

    results = fetch_range(days) 

    if not results: 

        print("⚠️ Không lấy được dữ liệu nào trong backfill.") 

        sys.exit(0) 

    # tiếp tục xử lý với results: viết vào file, phân tích 

    run([sys.executable, "analyze_excel.py"]) 

    run([sys.executable, "analysis.py"]) 

    run([sys.executable, "analysis_evolution.py"]) 

    run([sys.executable, "predict_xien.py"]) 

    print("✅ Backfill và phân tích hoàn tất.") 

 

 

if __name__ == "__main__": 

    import argparse 

    parser = argparse.ArgumentParser() 

    parser.add_argument('--backfill', type=int, help='Fetch lịch sử N ngày rồi phân tích') 

    parser.add_argument('--update-today', action='store_true', help='Cập nhật hôm nay nếu có kết quả web') 

    args = parser.parse_args() 

 

    if args.backfill: 

        backfill(args.backfill) 

    elif args.update_today: 

        update_today() 

    else: 

        print("Nothing to do. Sử dụng --backfill N hoặc --update-today") 
