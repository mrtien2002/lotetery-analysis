import os 

import pandas as pd 

 

print("📂 Current working dir:", os.getcwd()) 

print("📂 Files in dir:", os.listdir(".")) 

 

# Tìm file Excel có tên gần giống "du_lieu_goc" 

excel_files = [f for f in os.listdir(".") if f.endswith(".xlsx")] 

print("🔎 Excel files found:", excel_files) 

 

file_name = None 

for f in excel_files: 

    if "du_lieu_goc" in f:   # kiểm tra chuỗi "du_lieu_goc" 

        file_name = f 

        break 

 

if not file_name: 

    raise FileNotFoundError("❌ Không tìm thấy file Excel chứa 'du_lieu_goc'") 

 

print(f"✅ Đang đọc file: {file_name}") 

 

# Đọc dữ liệu từ Sheet1 

df = pd.read_excel(file_name, sheet_name="Sheet1", engine="openpyxl") 

 

print("✅ Đọc file thành công, số dòng:", len(df)) 

print("📌 5 dòng đầu:\n", df.head()) 

 

# --- Xử lý dữ liệu --- 

if "Ket_qua" not in df.columns or "Ngay" not in df.columns: 

    raise ValueError("❌ File Excel phải có 2 cột: 'Ngay' và 'Ket_qua'") 

 

# Tách cột Ket_qua thành nhiều cột 

df_split = df["Ket_qua"].astype(str).str.split(",", expand=True) 

 

# Đặt tên cột n1 -> n27 

df_split.columns = [f"n{i}" for i in range(1, df_split.shape[1] + 1)] 

 

# Gộp lại với cột Ngay 

df_final = pd.concat([df[["Ngay"]], df_split], axis=1) 

 

# Xuất ra file Excel mới 

output_file = "du_lieu_da_xu_ly.xlsx" 

with pd.ExcelWriter(output_file, engine="openpyxl") as writer: 

    df_final.to_excel(writer, sheet_name="ket_qua_hang_ngay", index=False) 

 

print(f"🎉 Đã tạo file {output_file} với sheet 'ket_qua_hang_ngay'") 
