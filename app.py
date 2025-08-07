import streamlit as st
from datetime import datetime
from skyfield.api import load, Topos
from pytz import timezone

# Load ephemeris data (use cache_resource because SpiceKernel is not pickle-able)
@st.cache_resource
def load_planets():
    return load('de421.bsp')  # Or 'de440s.bsp' if available

# UI Inputs
st.title("Astro Table Generator")
date_input = st.date_input("Select Date", value=datetime.now())
time_input = st.time_input("Select Time", value=datetime.now().time())
location = st.text_input("Enter Location (City, Country)", "Mumbai, India")

# Combine date and time into datetime object
dt = datetime.combine(date_input, time_input)

# Load planetary data
planets = load_planets()
ts = load.timescale()
t = ts.from_datetime(dt)

# Get coordinates using Nominatim (optional enhancement)
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="astro-app")
location_obj = geolocator.geocode(location)
if not location_obj:
    st.error("Location not found.")
    st.stop()

latitude = location_obj.latitude
longitude = location_obj.longitude
observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

# Compute planetary positions
planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
planet_positions = []

for name in planet_names:
    planet = planets[name]
    astrometric = (planets['earth'] + observer).at(t).observe(planet)
    ra, dec, distance = astrometric.radec()
    planet_positions.append((name, ra.hours, dec.degrees))

# Show on screen
st.subheader(f"Astrological Data for {location} on {dt.strftime('%Y-%m-%d %H:%M')}")
for name, ra, dec in planet_positions:
    st.write(f"{name}: RA = {ra:.2f}h, DEC = {dec:.2f}°")

# Export to PDF (optional)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

if st.button("Download PDF Report"):
    pdf_path = "/mnt/data/astro_report.pdf"
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    elements = [Paragraph(f"Astro Report for {location} on {dt}", styles["Title"])]
    for name, ra, dec in planet_positions:
        elements.append(Paragraph(f"{name}: RA = {ra:.2f}h, DEC = {dec:.2f}°", styles["Normal"]))
        elements.append(Spacer(1, 12))
    doc.build(elements)
    st.success("PDF generated!")
    st.download_button(label="📄 Download Astro Report", file_name="astro_report.pdf", mime="application/pdf", data=open(pdf_path, "rb").read())
