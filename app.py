# app.py
import streamlit as st
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import PLANETS
from datetime import datetime

st.set_page_config(page_title="Planetary Time & Price", layout="centered")

st.title("🔭 Planetary Time & Price Mapper")

# --- Input
symbol = st.text_input("Symbol (e.g., NIFTY):", value="NIFTY")
cmp = st.number_input("Current Market Price:", min_value=0.0, value=24596.0)
date = st.date_input("Select Date", value=datetime(2025, 8, 7))
time = st.time_input("Time (24H)", value=datetime.now().time())
lat = st.text_input("Latitude (e.g., 19.0760 for Mumbai):", value="19.0760")
lon = st.text_input("Longitude (e.g., 72.8777 for Mumbai):", value="72.8777")

if st.button("Calculate Planetary Degrees"):
    dt = Datetime(str(date), str(time)[:5], '+05:30')  # IST
    pos = GeoPos(lat, lon)
    chart = Chart(dt, pos)

    data = []
    for planet in PLANETS:
        obj = chart.get(planet)
        degree = round(obj.lon, 2)
        mapped_price = round((cmp * degree) / 360, 2)
        data.append({
            "Planet": planet,
            "Sign": obj.sign,
            "Degree": degree,
            "Mapped Price": mapped_price
        })

    # --- Show result
    st.subheader(f"🪐 Planetary Mapping for {symbol}")
    st.dataframe(data, use_container_width=True)
