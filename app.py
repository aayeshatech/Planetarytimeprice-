import streamlit as st
from skyfield.api import Loader, Topos
from datetime import datetime
import pytz
import pandas as pd

def get_planet_zodiac_deg(ra_hours):
    """Convert RA in hours to degrees in 0–360 zodiac range"""
    return (ra_hours * 15) % 360

def calculate_planetary_levels(input_price, trade_date, multiplier, latitude, longitude):
    # Load planetary data
    load = Loader('./skyfield_data')
    planets = load('de421.bsp')
    ts = load.timescale()

    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    planet_names = [
        ('Sun', 'sun'),
        ('Moon', 'moon'),
        ('Mercury', 'mercury'),
        ('Venus', 'venus'),
        ('Mars', 'mars'),
        ('Jupiter', 'jupiter barycenter'),
        ('Saturn', 'saturn barycenter')
    ]

    # Fix time to market open
    tz = pytz.timezone('Asia/Kolkata')
    calculation_time = tz.localize(trade_date.replace(hour=9, minute=15))
    t_utc = calculation_time.astimezone(pytz.utc)
    sky_t = ts.utc(t_utc.year, t_utc.month, t_utc.day, t_utc.hour, t_utc.minute)

    results = []
    degrees_list = []

    for display_name, planet_key in planet_names:
        planet = planets[planet_key]
        astrometric = observer.at(sky_t).observe(planet)
        apparent = astrometric.apparent()
        ra, dec, distance = apparent.radec()
        zodiac_deg = get_planet_zodiac_deg(ra.hours)

        level = input_price + zodiac_deg * multiplier
        degrees_list.append(zodiac_deg)

        results.append({
            'Planet': display_name,
            'Zodiac Degree': round(zodiac_deg, 2),
            'Price Level': round(level, 2)
        })

    # Combined calculation
    mean_deg = sum(degrees_list) / len(degrees_list)
    combined_level = input_price + mean_deg * multiplier

    return pd.DataFrame(results), round(mean_deg, 2), round(combined_level, 2)

# --- Streamlit UI ---
st.set_page_config(page_title="Planetary Price Calculator", layout="centered")
st.title("🌌 Combined Planetary Price Levels")

input_price = st.number_input("🔢 Enter input price (e.g. NIFTY)", value=24574, step=1)
trade_date = st.date_input("🗓️ Select trade date", datetime.now().date())
multiplier = st.number_input("📈 Degree to price multiplier", value=10.0, step=0.1)

st.markdown("#### 📍 Location for Calculation (default: Mumbai)")
latitude = st.number_input("Latitude", value=19.0760, format="%.6f")
longitude = st.number_input("Longitude", value=72.8777, format="%.6f")

if st.button("🚀 Calculate Planetary Levels"):
    trade_datetime = datetime.combine(trade_date, datetime.min.time())
    df, mean_deg, combined_price = calculate_planetary_levels(input_price, trade_datetime, multiplier, latitude, longitude)

    st.subheader("📊 Planet-wise Price Levels")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📌 Summary")
    st.write(f"**Mean Planetary Degree**: `{mean_deg}°`")
    st.write(f"**Combined Planetary Price Level**: `{combined_price}`")
