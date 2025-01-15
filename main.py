import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(layout="wide")

# 初始化地點資料
if "locations" not in st.session_state:
    st.session_state.locations = []
if "reload_flag" not in st.session_state:
    st.session_state.reload_flag = False

# Streamlit 標題
st.title("FishMap")

# 上傳 CSV 功能
st.sidebar.header("上傳地點資料 (CSV格式)")
uploaded_file = st.sidebar.file_uploader("選擇 CSV 文件", type="csv")
if uploaded_file is not None:
    try:
        # 手動指定 CSV 的欄位名稱
        column_names = ["地點", "lat", "lng"]
        data = pd.read_csv(uploaded_file, header=None, names=column_names)

        # 驗證資料並更新地點
        if {"地點", "lat", "lng"}.issubset(data.columns):
            st.session_state.locations = data.to_dict("records")
            st.session_state.reload_flag = not st.session_state.reload_flag  # 切換 flag 值觸發重渲染
            st.sidebar.success("成功讀入地點資料！")
        else:
            st.sidebar.error("CSV 資料必須包含三列 '地點', 'lat', 'lng'。")
    except Exception as e:
        st.sidebar.error(f"讀取 CSV 時發生錯誤: {e}")

# 地圖顯示
szs = 10
dzs = 14
if st.session_state.locations:
    latitudes = [loc["lat"] for loc in st.session_state.locations]
    longitudes = [loc["lng"] for loc in st.session_state.locations]
    center_lat = sum(latitudes) / len(latitudes)
    center_lng = sum(longitudes) / len(longitudes)
    m = folium.Map(location=[center_lat, center_lng], zoom_start=dzs)
else:
    m = folium.Map(location=[23.75, 120.25], zoom_start=szs)

# 添加地點標記
for loc in st.session_state.locations:
    folium.Marker(
        location=[loc["lat"], loc["lng"]],
        popup=loc["地點"],
        tooltip=loc["地點"]
    ).add_to(m)

st_folium(m, width=1024, height=600)
