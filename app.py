import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime
import pandas as pd
import pytz

# Title
st.title("🪐 Planetary Longitudes & Nifty Price Mapping")

# User inputs
date_input = st.date_input("Select Date", datetime.now().date())
time_input = st.time_input("Select Time", datetime.now().time())
location_input = st.text_input("Enter Location (e.g., Mumbai, India)", "Mumbai, India")

# Nifty price input
nifty_high = st.number_input("Nifty High", value=24634)
nifty_low = st.number_input("Nifty Low", value=24344)

# Compute timezone-aware datetime
timezone = pytz.timezone('Asia/Kolkata')
dt = timezone.localize(datetime.combine(date_input, time_input))

# Load planetary data
planets = load('de421.bsp')
ts = load.timescale()
t = ts.from_datetime(dt)

# Define planet list
planet_names = {
    "Sun": planets['sun'],
    "Moon": planets['moon'],
    "Mercury": planets['mercury'],
    "Venus": planets['venus'],
    "Mars": planets['mars'],
    "Jupiter": planets['jupiter barycenter'],
    "Saturn": planets['saturn barycenter'],
    "Rahu (Mean)": None,
    "Ketu (Mean)": None,
}

earth = planets['earth']

# Placeholder for table
planet_table = []

# Calculate Nifty range per degree
nifty_range = nifty_high - nifty_low
price_per_degree = nifty_range / 360

# Compute planetary longitudes and mapped price
for name, body in planet_names.items():
    if name == "Rahu (Mean)" or name == "Ketu (Mean)":
        # Approximate mean Rahu/Ketu longitude (reverse of Moon's node)
        moon = planets['moon']
        e = earth.at(t)
        moon_lon = e.observe(moon).ecliptic_latlon()[1].degrees
        rahu_lon = (moon_lon + 180) % 360
        ketu_lon = moon_lon % 360
        if name == "Rahu (Mean)":
            lon = rahu_lon
        else:
            lon = ketu_lon
    else:
        e = earth.at(t)
        astrometric = e.observe(body)
        lon = astrometric.ecliptic_latlon()[1].degrees

    sign = int(lon // 30) + 1
    mapped_price = nifty_low + (lon * price_per_degree)
    planet_table.append([name, round(lon, 2), sign, round(mapped_price, 2)])

# Display table
df = pd.DataFrame(planet_table, columns=["Planet", "Longitude (°)", "Sign", "Mapped Nifty Price"])
st.dataframe(df)

# Download as CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download as CSV", data=csv, file_name='planetary_nifty_mapping.csv', mime='text/csv')
