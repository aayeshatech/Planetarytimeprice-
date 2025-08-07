import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime
from geopy.geocoders import Nominatim
import pytz
import pandas as pd

# ---------------------------
@st.cache_data(show_spinner=False)
def get_location_coords(location_name):
    geolocator = Nominatim(user_agent="astro-app")
    location = geolocator.geocode(location_name)
    if location:
        timezone_str = pytz.country_timezones(location.raw['address']['country_code'])[0]
        return location.latitude, location.longitude, timezone_str
    return None, None, None

@st.cache_data(show_spinner=False)
def load_planets():
    return load('de421.bsp')  # you can use 'de422.bsp' for extended range

def get_planet_positions(date_str, time_str, lat, lon, tz_str):
    planets = load_planets()
    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

    local_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
    tz = pytz.timezone(tz_str)
    local_dt = tz.localize(local_time)
    utc_dt = local_dt.astimezone(pytz.utc)

    ts = load.timescale()
    t = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute)

    data = []
    for name in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter barycenter', 'saturn barycenter']:
        body = planets[name]
        astrometric = observer.at(t).observe(body).apparent()
        ra, dec, distance = astrometric.radec()
        alt, az, _ = astrometric.altaz()
        data.append({
            'Planet': name.title(),
            'RA (hrs)': round(ra.hours, 4),
            'Dec (°)': round(dec.degrees, 4),
            'Altitude (°)': round(alt.degrees, 4)
        })

    return pd.DataFrame(data)

# ---------------------------
st.set_page_config(page_title="Astro Timeline Tool", layout="centered")
st.title("🪐 Planetary Timeline - Astrology Astro Date Tool")

col1, col2 = st.columns(2)
with col1:
    date_input = st.date_input("📅 Select Date", datetime.now()).strftime("%d-%m-%Y")
with col2:
    time_input = st.time_input("⏰ Select Time", datetime.now().time()).strftime("%H:%M")

location_input = st.text_input("📍 Location (e.g., Mumbai, India)", "Mumbai, India")

if st.button("🔮 Show Planet Positions"):
    lat, lon, tz_str = get_location_coords(location_input)
    if lat is None:
        st.error("❌ Location not found.")
    else:
        df = get_planet_positions(date_input, time_input, lat, lon, tz_str)
        st.markdown("### 🌠 Planetary Positions")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download as CSV", data=csv, file_name="planet_positions.csv", mime="text/csv")
