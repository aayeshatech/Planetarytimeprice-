import streamlit as st
from skyfield.api import Loader, Topos
from datetime import datetime
import pytz

def calculate_combined_planetary_level(input_price, trade_date, multiplier, latitude, longitude):
    load = Loader('./skyfield_data')
    planets = load('de421.bsp')
    ts = load.timescale()

    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    planet_names = [
        'sun',
        'moon',
        'mercury',
        'venus',
        'mars',
        'jupiter barycenter',
        'saturn barycenter'
    ]
    
    tz = pytz.timezone('Asia/Kolkata')
    calculation_time = tz.localize(trade_date.replace(hour=9, minute=15))  # Use single time like market open
    
    t_utc = calculation_time.astimezone(pytz.utc)
    sky_t = ts.utc(t_utc.year, t_utc.month, t_utc.day, t_utc.hour, t_utc.minute)
    
    degrees_list = []
    for planet_key in planet_names:
        planet_obj = planets[planet_key]
        astrometric = observer.at(sky_t).observe(planet_obj)
        apparent = astrometric.apparent()
        ra, dec, distance = apparent.radec()
        deg = ra.hours * 15  # Convert RA hour to degrees
        degrees_list.append(deg)
    
    mean_deg = sum(degrees_list) / len(degrees_list)
    combined_level = input_price + mean_deg * multiplier
    
    return round(combined_level, 2), round(mean_deg, 2)

# Streamlit UI
st.title("Single Combined Planetary Level")

input_price = st.number_input("Enter input price (e.g. NIFTY price)", value=24574, step=1)
trade_date = st.date_input("Select trade date", datetime.now().date())
multiplier = st.number_input("Degree to price multiplier", value=10.0, step=0.1)

latitude = st.number_input("Latitude", value=19.0760, format="%.6f")
longitude = st.number_input("Longitude", value=72.8777, format="%.6f")

if st.button("Calculate Combined Level"):
    trade_date_dt = datetime.combine(trade_date, datetime.min.time())
    level, mean_degree = calculate_combined_planetary_level(input_price, trade_date_dt, multiplier, latitude, longitude)
    st.write(f"Mean planetary degree: {mean_degree}°")
    st.write(f"Combined planetary price level: {level}")
