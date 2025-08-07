import streamlit as st
from skyfield.api import Loader, Topos
from datetime import datetime
import pytz

def calculate_levels(input_price, trade_date, multiplier, latitude, longitude):
    load = Loader('./skyfield_data')
    planets = load('de421.bsp')
    ts = load.timescale()

    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    tz = pytz.timezone('Asia/Kolkata')
    times_ist = [
        tz.localize(trade_date.replace(hour=9, minute=15)),
        tz.localize(trade_date.replace(hour=14, minute=15)),
    ]

    results = []
    for t in times_ist:
        t_utc = t.astimezone(pytz.utc)
        sky_t = ts.utc(t_utc.year, t_utc.month, t_utc.day, t_utc.hour, t_utc.minute)
        for planet in planet_names:
            planet_obj = planets[planet]
            astrometric = observer.at(sky_t).observe(planet_obj)
            apparent = astrometric.apparent()
            ra, dec, distance = apparent.radec()
            deg = ra.hours * 15  # degrees
            level = input_price + deg * multiplier
            results.append({
                "time": t.strftime('%H:%M'),
                "planet": planet,
                "degree": round(deg, 2),
                "level": round(level, 2)
            })
    return results

# Streamlit UI
st.title("Intraday Planetary Levels for Trading")

input_price = st.number_input("Enter input price (e.g. NIFTY price)", value=24574)
trade_date = st.date_input("Select trade date", datetime.now().date())
multiplier = st.number_input("Degree to price multiplier", value=10)
latitude = st.number_input("Latitude", value=19.0760)    # default Mumbai
longitude = st.number_input("Longitude", value=72.8777)  # default Mumbai

if st.button("Generate Levels"):
    # Convert date input to datetime (with dummy time for tz management)
    trade_date_dt = datetime.combine(trade_date, datetime.min.time())
    levels = calculate_levels(input_price, trade_date_dt, multiplier, latitude, longitude)

    st.write(f"Intraday planetary levels for {trade_date.strftime('%Y-%m-%d')}:")
    st.table(levels)
