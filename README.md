# Lottery Analysis Project

Dự án này thu thập và phân tích kết quả xổ số miền Bắc (XSMB) hằng ngày, lưu vào Google Sheets và tạo bảng phân tích.

## Cách chạy

### Backfill 300 ngày
```bash
python pipeline.py --backfill 300
```

### Cập nhật hôm nay
```bash
python pipeline.py --update-today
```
