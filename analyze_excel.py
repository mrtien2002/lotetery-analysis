import pandas as pd 

import os 

 

# Tìm file Excel gốc 

fname = "dulieu.xlsx" 

if not os.path.exists(fname): 

    raise FileNotFoundError(f"❌ Không tìm thấy file {fname}") 

 

# Đọc dữ liệu gốc 

df = pd.read_excel(fname, sheet_name="Sheet1") 

 

# --- Xử lý sheet ket_qua_hang_ngay --- 

df_split = df['Ket_qua'].str.split(',', expand=True) 

df_split.columns = [f"n{i}" for i in range(1, df_split.shape[1] + 1)] 

df_final = pd.concat([df[['Ngay']], df_split], axis=1) 

 

# --- Phân tích Max/Trung/Min --- 

df_final_melt = df_final.melt(id_vars=["Ngay"], value_name="So").dropna() 

df_final_melt["So"] = df_final_melt["So"].str.strip() 

 

# Tạo cột tháng 

df_final_melt["Thang"] = pd.to_datetime(df_final_melt["Ngay"]).dt.to_period("M") 

 

# Đếm tần suất theo tháng 

counts = df_final_melt.groupby(["Thang", "So"]).size().reset_index(name="So_lan") 

 

# Gắn nhãn Max / Trung / Min 

def classify(x): 

    if x >= 9: 

        return "MAX" 

    elif x >= 5: 

        return "TRUNG" 

    else: 

        return "MIN" 

 

counts["Nhom"] = counts["So_lan"].apply(classify) 

 

# Ghi ra file mới 

with pd.ExcelWriter("dulieu_xuly.xlsx", engine="openpyxl") as writer: 

    df_final.to_excel(writer, sheet_name="ket_qua_hang_ngay", index=False) 

    counts.to_excel(writer, sheet_name="phan_tich", index=False) 

 

print("✅ Đã tạo file dulieu_xuly.xlsx với 2 sheet: ket_qua_hang_ngay + phan_tich") 
