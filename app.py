import swisseph as swe
import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
import io
import matplotlib.pyplot as plt

# Set ephemeris path
swe.set_ephe_path('/usr/share/ephe')

# Planet names for display
PLANETS = [
    (swe.SUN, 'Sun'),
    (swe.MOON, 'Moon'),
    (swe.MERCURY, 'Mercury'),
    (swe.VENUS, 'Venus'),
    (swe.MARS, 'Mars'),
    (swe.JUPITER, 'Jupiter'),
    (swe.SATURN, 'Saturn'),
    (swe.URANUS, 'Uranus'),
    (swe.NEPTUNE, 'Neptune'),
    (swe.PLUTO, 'Pluto')
]

# Function to get timezone from location
def get_timezone(location):
    geolocator = Nominatim(user_agent="astro_app")
    loc = geolocator.geocode(location)
    if loc is None:
        return None, None, None
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
    return timezone_str, loc.latitude, loc.longitude

# Function to calculate planetary positions
def calculate_positions(date_str, time_str, location):
    timezone_str, lat, lon = get_timezone(location)
    if not timezone_str:
        st.error("Invalid location.")
        return None

    # Convert to UTC
    local = pytz.timezone(timezone_str)
    local_dt = local.localize(datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M"))
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

    result = []
    for planet_id, planet_name in PLANETS:
        lon, _ = swe.calc_ut(jd, planet_id)
        result.append((planet_name, round(lon[0], 2)))  # lon is a tuple; use lon[0]

    return result, lat, lon

# Streamlit UI
st.title("🪐 Planetary Time & Price Astro Report")

date_input = st.date_input("Select Date", datetime.today())
time_input = st.time_input("Select Time", datetime.now().time())
location_input = st.text_input("Enter Location (City, Country)", "Mumbai, India")

if st.button("Generate Astro Report"):
    date_str = date_input.strftime("%Y/%m/%d")
    time_str = time_input.strftime("%H:%M")
    data, lat, lon = calculate_positions(date_str, time_str, location_input)
    if data:
        st.subheader("🌠 Planetary Positions (Longitude)")
        for planet, pos in data:
            st.write(f"**{planet}**: {pos}°")

        # Show chart
        fig, ax = plt.subplots()
        names = [item[0] for item in data]
        positions = [item[1] for item in data]
        ax.barh(names, positions)
        ax.set_xlabel("Longitude (°)")
        st.pyplot(fig)

        # PDF Export
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = [Paragraph("🪐 Planetary Astro Report", styles["Title"]),
                    Spacer(1, 12),
                    Paragraph(f"Date: {date_str} {time_str}", styles["Normal"]),
                    Paragraph(f"Location: {location_input}", styles["Normal"]),
                    Spacer(1, 12)]
        for planet, pos in data:
            elements.append(Paragraph(f"{planet}: {pos}°", styles["Normal"]))
        doc.build(elements)
        st.download_button("📥 Download PDF Report", pdf_buffer.getvalue(), "astro_report.pdf", "application/pdf")
