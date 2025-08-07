import streamlit as st
from skyfield.api import Loader, Topos
from datetime import datetime
import pytz

def calculate_upper_lower_levels(input_price, trade_date, multiplier, latitude, longitude):
    load = Loader('./skyfield_data')
    planets = load('de421.bsp')
    ts = load.timescale()

    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    
    # Correct planet keys for Skyfield ephemeris
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
    
    tz = pytz.timezone('Asia/Kolkata')
    # Use 9:15 AM IST as intraday time for calculation
    times_ist = [
        tz.localize(trade_date.replace(hour=9, minute=15)),
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
            deg = ra.hours * 15  # Convert RA hours to degrees
            
            upper = input_price + deg * multiplier
            lower = input_price - deg * multiplier
            
            results.append({
                "Time (IST)": t.strftime('%H:%M'),
                "Planet": display_names[planet_key],
                "Degree": round(deg, 2),
                "Upper Level": round(upper, 2),
                "Lower Level": round(lower, 2)
            })
    return results

st.title("Intraday Planetary Levels with Upper & Lower Support/Resistance")

input_price = st.number_input("Enter input price (e.g. NIFTY price)", value=24574, step=1)
today_low = st.number_input("Enter today's market low (for reference)", value=24344, step=1)
trade_date = st.date_input("Select trade date", datetime.now().date())
multiplier = st.number_input("Degree to price multiplier", value=10.0, step=0.1)

latitude = st.number_input("Latitude", value=19.0760, format="%.6f")
longitude = st.number_input("Longitude", value=72.8777, format="%.6f")

if st.button("Generate Levels"):
    trade_date_dt = datetime.combine(trade_date, datetime.min.time())
    levels = calculate_upper_lower_levels(input_price, trade_date_dt, multiplier, latitude, longitude)
    
    st.subheader(f"Planetary Levels for {trade_date.strftime('%Y-%m-%d')} at 09:15 IST")
    
    # Display full table
    st.table(levels)
    
    # Show lower levels near/below today's low to identify possible supports
    filtered = [l for l in levels if l["Lower Level"] <= today_low]
    if filtered:
        st.subheader("Lower Levels Near or Below Today's Market Low (Potential Supports):")
        st.table(filtered)
    else:
        st.info("No lower planetary levels found near or below today's market low.")

