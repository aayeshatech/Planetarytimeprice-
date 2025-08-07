# app.py
import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime
import pytz

st.title("🪐 Planetary Timeline - Astrology Astro Date Tool")

# User Input
date_input = st.date_input("📅 Select Date", datetime.now().date())
time_input = st.time_input("⏰ Select Time", datetime.now().time())
location_input = st.text_input("📍 Location (e.g., Mumbai, India)", "Mumbai, India")

# Convert to UTC
local_tz = pytz.timezone('Asia/Kolkata')  # You can auto-detect later
dt_local = local_tz.localize(datetime.combine(date_input, time_input))
dt_utc = dt_local.astimezone(pytz.utc)

# Load planetary data
planets = load('de421.bsp')
earth = planets['earth']
ts = load.timescale()
t = ts.utc(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour, dt_utc.minute)

# Topos (approx Mumbai coords)
observer = earth + Topos(latitude_degrees=19.0760, longitude_degrees=72.8777)

# Planets to observe
planet_list = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter barycenter', 'saturn barycenter']
positions = []

for name in planet_list:
    planet = planets[name]
    astrometric = observer.at(t).observe(planet).apparent()
    ra, dec, distance = astrometric.radec()
    alt, az, _ = observer.at(t).observe(planet).apparent().altaz()
    positions.append((name.title(), ra.hours, dec.degrees, alt.degrees))

# Display table
st.subheader("🌠 Planetary Positions")
st.table([
    {"Planet": name, "RA (hrs)": round(ra, 2), "Dec (°)": round(dec, 2), "Altitude (°)": round(alt, 2)}
    for name, ra, dec, alt in positions
])
