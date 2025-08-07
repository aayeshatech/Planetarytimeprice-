# streamlit_app.py

import streamlit as st
from datetime import datetime
from skyfield.api import load, Topos
from pytz import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import io

st.set_page_config(page_title="Astro Market Report", layout="centered")

st.title("🔭 Astro Market Transit Report")

# --- 1. INPUT ---
st.subheader("📅 Enter Date & Time")
date_input = st.date_input("Select Date", datetime.now().date())
time_input = st.time_input("Select Time", datetime.now().time())

st.subheader("📍 Location")
location = st.text_input("Enter Location (e.g., Mumbai, India)", "Mumbai, India")

st.subheader("📈 Market Levels (Optional)")
nifty_high = st.number_input("Nifty High", value=24640)
nifty_low = st.number_input("Nifty Low", value=24344)

# --- 2. BUTTON ---
if st.button("🔁 Generate Report"):

    # --- 3. ASTRO LOGIC ---
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="geoapi")
        location_obj = geolocator.geocode(location)
        if not location_obj:
            st.error("Location not found.")
        else:
            latitude = location_obj.latitude
            longitude = location_obj.longitude
            dt = datetime.combine(date_input, time_input)
            ts = load.timescale()
            t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)
            eph = load('de421.bsp')

            planets = {
                'Sun': eph['sun'],
                'Moon': eph['moon'],
                'Mercury': eph['mercury'],
                'Venus': eph['venus'],
                'Mars': eph['mars'],
                'Jupiter': eph['jupiter barycenter'],
                'Saturn': eph['saturn barycenter']
            }

            observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
            astrological_data = []

            for name, planet in planets.items():
                astrometric = eph['earth'] + observer
                planet_pos = astrometric.at(t).observe(planet).apparent()
                ra, dec, distance = planet_pos.radec()
                astrological_data.append([name, round(ra.hours, 2), round(dec.degrees, 2)])

            # --- 4. SHOW TABLE ---
            st.subheader("📊 Planetary Positions")
            st.table([["Planet", "RA (hrs)", "Dec (deg)"]] + astrological_data)

            # --- 5. DOWNLOAD REPORT PDF ---
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            elements.append(Paragraph("Astro Market Transit Report", styles['Title']))
            elements.append(Paragraph(f"Date: {dt.strftime('%Y-%m-%d %H:%M')} | Location: {location}", styles['Normal']))
            elements.append(Spacer(1, 12))

            table_data = [["Planet", "RA (hrs)", "Dec (deg)"]] + astrological_data
            elements.append(Table(table_data))

            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Nifty High: {nifty_high} | Nifty Low: {nifty_low}", styles['Normal']))

            doc.build(elements)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Report as PDF",
                data=buffer,
                file_name=f"astro_market_report_{dt.strftime('%Y%m%d_%H%M')}.pdf",
                mime='application/pdf'
            )

    except Exception as e:
        st.error(f"Error: {e}")
