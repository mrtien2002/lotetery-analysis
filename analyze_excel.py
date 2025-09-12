import pandas as pd 

 

# Đọc file gốc (ở thư mục gốc repo) 

df = pd.read_excel("du_lieu_goc.xlsx", sheet_name="Sheet1") 

 

# Tách cột Ket_qua thành danh sách các số 

df_split = df['Ket_qua'].str.split(',', expand=True) 

 

# Đặt tên cột n1 -> n27 

df_split.columns = [f"n{i}" for i in range(1, df_split.shape[1] + 1)] 

 

# Gộp lại với cột Ngay 

df_final = pd.concat([df[['Ngay']], df_split], axis=1) 

 

# Ghi ra file mới với sheet ket_qua_hang_ngay 

with pd.ExcelWriter("du_lieu_da_xu_ly.xlsx", engine="openpyxl") as writer: 

    df_final.to_excel(writer, sheet_name="ket_qua_hang_ngay", index=False) 

 

print("✅ Đã tạo file du_lieu_da_xu_ly.xlsx với sheet ket_qua_hang_ngay") 
