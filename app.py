import streamlit as st
from datetime import datetime
from skyfield.api import load, Topos
from geopy.geocoders import Nominatim
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# Title
st.title("🪐 Planetary Time & Location Viewer")

# Input form
with st.form("input_form"):
    input_datetime_str = st.text_input("Enter Date & Time (e.g., 7-8-2025 9:15 AM)", "7-8-2025 9:15 AM")
    location_input = st.text_input("Enter Location (e.g., Mumbai, India)", "Mumbai, India")
    submitted = st.form_submit_button("Show Planetary Info")

if submitted:
    try:
        # Parse input datetime
        dt = datetime.strptime(input_datetime_str, "%d-%m-%Y %I:%M %p")

        # Geocode location
        geolocator = Nominatim(user_agent="planetary_app")
        location = geolocator.geocode(location_input)
        if not location:
            st.error("Could not find location.")
        else:
            latitude = location.latitude
            longitude = location.longitude
            st.success(f"Coordinates: {latitude}, {longitude}")

            # Skyfield load
            eph = load('de421.bsp')
            ts = load.timescale()
            t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)

            planets = {
                "Sun": eph["sun"],
                "Moon": eph["moon"],
                "Mercury": eph["mercury"],
                "Venus": eph["venus"],
                "Mars": eph["mars"],
                "Jupiter": eph["jupiter barycenter"],
                "Saturn": eph["saturn barycenter"]
            }

            earth = eph["earth"]
            observer = earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

            planet_data = []
            for name, planet in planets.items():
                astrometric = observer.at(t).observe(planet).apparent()
                alt, az, distance = astrometric.altaz()
                planet_data.append((name, alt.degrees, az.degrees))

            # Show results
            st.subheader("🪐 Planetary Positions (Altitude & Azimuth):")
            for name, alt, az in planet_data:
                st.write(f"{name}: Altitude = {alt:.2f}°, Azimuth = {az:.2f}°")

            # Create PDF
            pdf_filename = "/mnt/data/planetary_positions.pdf"
            doc = SimpleDocTemplate(pdf_filename)
            styles = getSampleStyleSheet()
            elements = [Paragraph("Planetary Positions", styles["Title"]), Spacer(1, 12)]

            for name, alt, az in planet_data:
                text = f"{name}: Altitude = {alt:.2f}°, Azimuth = {az:.2f}°"
                elements.append(Paragraph(text, styles["Normal"]))
                elements.append(Spacer(1, 6))

            doc.build(elements)

            st.success("PDF generated!")
            st.download_button(label="📄 Download PDF", file_name="planetary_positions.pdf", mime="application/pdf", data=open(pdf_filename, "rb").read())

    except ValueError as e:
        st.error(f"Error: {str(e)}. Ensure your date format is: `7-8-2025 9:15 AM`")

