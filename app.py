import streamlit as st
from skyfield.api import Loader, Topos
from datetime import datetime
import pytz
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# Skyfield loader
load = Loader('./skyfield_data')
planets = load('de421.bsp')
ts = load.timescale()

# Planet list
planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

# Title
st.title("🪐 Planetary Position Report")

# User inputs
date_input = st.date_input("Enter Date", datetime.now().date())
time_input = st.time_input("Enter Time", datetime.now().time())
location_input = st.text_input("Enter Location (City, Country)", "Mumbai, India")

# Geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="astro_app")

# Process button
if st.button("Generate Report"):
    # Convert input to datetime
    dt = datetime.combine(date_input, time_input)

    # Make datetime timezone-aware (UTC)
    local_tz = pytz.timezone('Asia/Kolkata')  # You can change based on location
    local_dt = local_tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    # Skyfield time object
    t = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute)

    # Resolve location
    location = geolocator.geocode(location_input)
    if not location:
        st.error("Location not found.")
    else:
        observer = Topos(latitude_degrees=location.latitude, longitude_degrees=location.longitude)
        earth = planets['earth']
        obs = earth + observer

        # Generate planetary positions
        output = []
        for name in planet_names:
            astrometric = obs.at(t).observe(planets[name])
            apparent = astrometric.apparent()
            ra, dec, distance = apparent.radec()
            alt, az, _ = apparent.altaz()
            output.append((name, round(az.degrees, 2), round(alt.degrees, 2)))

        # Show result
        st.subheader("🌌 Planetary Positions")
        for planet, az, alt in output:
            st.write(f"**{planet}** — Azimuth: {az}°, Altitude: {alt}°")

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = [Paragraph("🪐 Planetary Report", styles['Title']),
                    Paragraph(f"Date: {dt.strftime('%Y-%m-%d %H:%M')} ({location_input})", styles['Normal']),
                    Spacer(1, 12)]
        for planet, az, alt in output:
            elements.append(Paragraph(f"{planet} — Azimuth: {az}°, Altitude: {alt}°", styles['Normal']))
            elements.append(Spacer(1, 6))
        doc.build(elements)
        buffer.seek(0)

        # Download PDF
        st.download_button("📄 Download PDF", data=buffer, file_name="planetary_report.pdf", mime="application/pdf")
