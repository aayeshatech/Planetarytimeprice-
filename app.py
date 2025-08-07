import swisseph as swe
import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

# Initialize Streamlit app
st.set_page_config(page_title="Astro Planetary Report", layout="centered")

# Title
st.title("🪐 Planetary Time & Price Astro Report")

# Input: Date, Time, Location
with st.form("astro_form"):
    date_input = st.date_input("Select Date", value=datetime.now().date())
    time_input = st.time_input("Select Time", value=datetime.now().time())
    location_input = st.text_input("Enter Location (City, Country)", value="Mumbai, India")
    submitted = st.form_submit_button("Generate Astro Report")

if submitted:
    try:
        # Get timezone from location
        geolocator = Nominatim(user_agent="astro_app")
        location = geolocator.geocode(location_input)

        if not location:
            st.error("Location not found. Please try again.")
        else:
            lat = location.latitude
            lon = location.longitude

            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lng=lon, lat=lat)
            tz = pytz.timezone(timezone_str)

            dt = tz.localize(datetime.combine(date_input, time_input))
            julian_day = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

            planet_names = [
                "Sun", "Moon", "Mercury", "Venus", "Mars",
                "Jupiter", "Saturn", "Rahu", "Ketu"
            ]

            planet_numbers = [
                swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
                swe.JUPITER, swe.SATURN, swe.MEAN_NODE, -1  # -1 for Ketu
            ]

            planetary_positions = []

            for i, p in enumerate(planet_numbers):
                if p == -1:  # Ketu
                    rahu = swe.calc_ut(julian_day, swe.MEAN_NODE)[0]
                    ketu = (rahu + 180) % 360
                    planetary_positions.append((planet_names[i], round(ketu, 2)))
                else:
                    pos = swe.calc_ut(julian_day, p)[0]
                    planetary_positions.append((planet_names[i], round(pos, 2)))

            # Display Results
            st.subheader("🪐 Planetary Positions:")
            for planet, pos in planetary_positions:
                st.write(f"**{planet}**: {pos}°")

            # Plot planetary positions (optional)
            fig, ax = plt.subplots()
            labels = [p[0] for p in planetary_positions]
            values = [p[1] for p in planetary_positions]
            ax.barh(labels, values)
            ax.set_xlabel("Degree")
            ax.set_title("Planetary Positions (Degrees)")
            st.pyplot(fig)

            # Generate PDF
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            elements.append(Paragraph("🪐 Astro Planetary Report", styles["Title"]))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Location: {location_input}", styles["Normal"]))
            elements.append(Paragraph(f"Date/Time: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}", styles["Normal"]))
            elements.append(Spacer(1, 12))

            for planet, pos in planetary_positions:
                elements.append(Paragraph(f"{planet}: {pos}°", styles["Normal"]))

            doc.build(elements)
            st.download_button("📄 Download PDF Report", data=pdf_buffer.getvalue(), file_name="astro_report.pdf")

    except Exception as e:
        st.error(f"Error: {str(e)}")
