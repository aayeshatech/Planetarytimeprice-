import streamlit as st
from skyfield.api import load
import pandas as pd
from datetime import datetime
import pytz

# Load ephemeris
planets = load('de421.bsp')
ts = load.timescale()

# Input section
st.title("🔮 Astro Intraday Price & Time System")

symbol = st.text_input("Enter Symbol (e.g., Nifty)", "Nifty")
cmp = st.number_input("CMP or Close Price", value=24596.0)
high = st.number_input("High", value=24634.0)
low = st.number_input("Low", value=24344.0)
date_input = st.date_input("Select Date", datetime.now().date())
time_input = st.time_input("Select Time", datetime.now().time())
location = st.text_input("Location (City)", "Mumbai")

# Timezone
timezone = pytz.timezone("Asia/Kolkata")
dt = timezone.localize(datetime.combine(date_input, time_input))
t = ts.from_datetime(dt)

# Planet list
planet_dict = {
    "Sun": planets['sun'],
    "Moon": planets['moon'],
    "Mercury": planets['mercury'],
    "Venus": planets['venus'],
    "Mars": planets['mars'],
    "Jupiter": planets['jupiter barycenter'],
    "Saturn": planets['saturn barycenter'],
    "Uranus": planets['uranus barycenter'],
    "Neptune": planets['neptune barycenter'],
    "Pluto": planets['pluto barycenter']
}

# Price per degree
price_range = high - low
price_per_deg = price_range / 360

# Result table
results = []
earth = planets['earth']

for name, planet in planet_dict.items():
    astrometric = earth.at(t).observe(planet)
    lon = astrometric.ecliptic_latlon()[1].degrees
    price_level = low + (lon * price_per_deg)
    results.append([name, round(lon, 2), round(price_level, 2)])

# Output DataFrame
df = pd.DataFrame(results, columns=["Planet", "Longitude (°)", f"{symbol} Price Level"])
st.dataframe(df)

# Download CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, f"{symbol}_astro_levels.csv", "text/csv")
