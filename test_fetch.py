def fetch_minhngoc(d: date): 

    # URL kết quả Miền Bắc theo ngày 

    url = f"https://www.minhngoc.net.vn/ket-qua-xo-so/mien-bac/{d.strftime('%d-%m-%Y')}.html" 

    r = requests.get(url, headers=HEADERS, timeout=30) 

    r.raise_for_status() 

    soup = BeautifulSoup(r.text, 'lxml') 

 

    # Tìm khu vực bảng kết quả có id="kqmb" 

    container = soup.find(id='kqmb') 

    if not container: 

        raise RuntimeError("Không tìm thấy khung kết quả kqmb") 

 

    # Lấy tất cả số trong bảng (chỉ lấy thẻ <td> hoặc <div> có chứa số) 

    nums = [] 

    for td in container.find_all(['td', 'div']): 

        txt = td.get_text(strip=True) 

        if txt.isdigit():  # chỉ giữ các ô toàn số 

            if len(txt) >= 2: 

                nums.append(txt[-2:])  # chỉ lấy 2 số cuối 

 

    # Sau khi lọc phải còn đúng 27 số 

    if len(nums) != 27: 

        raise RuntimeError(f"Sai số lượng: {len(nums)} số thay vì 27") 

 

    return nums 
