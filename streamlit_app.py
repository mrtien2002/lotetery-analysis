import os
import streamlit as st
import pandas as pd
from gsheets_utils import open_spreadsheet, ensure_worksheet, read_dataframe

st.set_page_config(page_title='XS Analysis', page_icon='🎯', layout='wide')

st.title('Phân tích xổ số (thống kê) – Demo')
st.caption('Nguồn: Google Sheets • Phân tích: tần suất, số khan, Method 1 & 2')

@st.cache_data(ttl=300)
def load_analysis():
    ss = open_spreadsheet()
    ws = ensure_worksheet(ss, 'analysis_today')
    df = read_dataframe(ws)
    # coerce types
    num_cols = [c for c in df.columns if c not in ['number','group_method2']]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

df = load_analysis()
if df is None or df.empty:
    st.warning('Chưa có dữ liệu. Hãy chạy backfill/update trước.')
else:
    left, right = st.columns([1,3])
    with left:
        st.subheader('Bộ lọc')
        group = st.multiselect('Nhóm (Method 2)', ['MAX','TRUNG','MIN'], default=['MAX','TRUNG','MIN'])
        khan_only = st.checkbox('Chỉ số khan (>=7 ngày)')
        sort_by = st.selectbox('Sắp xếp theo', ['freq_30d','freq_60d','freq_90d','freq_300d','last_seen_days','method1_score_month','method2_points'])
        topk = st.slider('Hiển thị top', 5, 100, 30)

    view = df.copy()
    if group:
        view = view[view['group_method2'].isin(group)]
    if khan_only:
        view = view[view['khan_ge7'] == True]
    view = view.sort_values(by=sort_by, ascending=False).head(topk)

    with right:
        st.subheader('Bảng kết quả')
        st.dataframe(view, hide_index=True, use_container_width=True)

    st.divider()
    st.caption('Lưu ý pháp lý: Đây là công cụ thống kê công khai, không hỗ trợ hay khuyến khích cá cược.')
