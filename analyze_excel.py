import pandas as pd 

 

# Đọc file gốc 

df = pd.read_excel("dulieu.xlsx", sheet_name="Sheet1", engine="openpyxl") 

 

# Tách cột Ket_qua thành 27 số riêng 

df_split = df['Ket_qua'].str.split(',', expand=True) 

df_split.columns = [f"n{i}" for i in range(1, df_split.shape[1] + 1)] 

 

# Ghép lại với cột Ngay 

df_final = pd.concat([df[['Ngay']], df_split], axis=1) 

 

# Xuất ra file mới 

output_file = "dulieu_xuly.xlsx" 

with pd.ExcelWriter(output_file, engine="openpyxl") as writer: 

    df_final.to_excel(writer, sheet_name="ket_qua_hang_ngay", index=False) 

 

# In 5 dòng đầu để kiểm tra 

print("✅ Đã tạo file", output_file) 

print(df_final.head()) 
