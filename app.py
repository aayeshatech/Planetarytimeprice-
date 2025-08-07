import streamlit as st
from skyfield.api import Loader, Topos
from datetime import datetime
import pytz

def calculate_levels(input_price, trade_date, multiplier, latitude, longitude):
    load = Loader('./skyfield_data')  # cache folder for ephemeris data
    planets = load('de421.bsp')
    ts = load.timescale()

    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    
    # Correct keys as per Skyfield ephemeris de421.bsp
    planet_names = [
        'sun',
        'moon',
        'mercury',
        'venus',
        'mars',
        'jupiter barycenter',
        'saturn barycenter'
    ]
    display_names = {
        'sun': 'Sun',
        'moon': 'Moon',
        'mercury': 'Mercury',
        'venus': 'Venus',
        'mars': 'Mars',
        'jupiter barycenter': 'Jupiter',
        'saturn barycenter': 'Saturn'
    }
    
    # Define 5-hour frequency times (IST) - adjust as needed
    tz = pytz.timezone('Asia/Kolkata')
    times_ist = [
        tz.localize(trade_date.replace(hour=9, minute=15)),
        tz.localize(trade_date.replace(hour=14, minute=15)),
        # Optionally add more times here
    ]
    
    results = []
    for t in times_ist:
        t_utc = t.astimezone(pytz.utc)
        sky_t = ts.utc(t_utc.year, t_utc.month, t_utc.day, t_utc.hour, t_utc.minute)
        
        for planet_key in planet_names:
            planet_obj = planets[planet_key]
            astrometric = observer.at(sky_t).observe(planet_obj)
            apparent = astrometric.apparent()
            ra, dec, distance = apparent.radec()
            deg = ra.hours * 15  # Right ascension hours to degrees
            
            level = input_price + deg * multiplier
            
            results.append({
                "Time (IST)": t.strftime('%H:%M'),
                "Planet": display_names[planet_key],
                "Degree": round(deg, 2),
                "Level": round(level, 2)
            })
    return results

# Streamlit UI
st.title("Intraday Planetary Levels for Trading")

input_price = st.number_input("Enter input price (e.g. NIFTY price)", value=24574, step=1)
trade_date = st.date_input("Select trade date", datetime.now().date())
multiplier = st.number_input("Degree to price multiplier", value=10.0, step=0.1)

latitude = st.number_input("Latitude", value=19.0760, format="%.6f")
longitude = st.number_input("Longitude", value=72.8777, format="%.6f")

if st.button("Generate Levels"):
    trade_date_dt = datetime.combine(trade_date, datetime.min.time())
    levels = calculate_levels(input_price, trade_date_dt, multiplier, latitude, longitude)
    
    st.subheader(f"Planetary Levels for {trade_date.strftime('%Y-%m-%d')}")
    st.table(levels)
