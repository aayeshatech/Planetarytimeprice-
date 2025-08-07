import streamlit as st
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from geopy.geocoders import Nominatim
import pytz
import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime as dt


# --- Helper: Get Lat/Long/Timezone from Location ---
@st.cache_data(show_spinner=False)
def get_location_data(location_name):
    geolocator = Nominatim(user_agent="astro-app")
    location = geolocator.geocode(location_name)
    if location:
        timezone = pytz.timezone(pytz.country_timezones(location.raw['address']['country_code'])[0])
        return {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'timezone': str(timezone)
        }
    return None

# --- Helper: Create Astro Table Data ---
def create_astro_table(date_str, time_str, location_data):
    date_time_obj = dt.strptime(f"{date_str} {time_str}", "%d-%m-%Y %I:%M %p")
    timezone = pytz.timezone(location_data['timezone'])
    local_dt = timezone.localize(date_time_obj)
    utc_dt = local_dt.astimezone(pytz.utc)

    # Flatlib Datetime and Chart
    fdatetime = Datetime(utc_dt.strftime("%Y/%m/%d"), utc_dt.strftime("%H:%M"))
    pos = GeoPos(str(location_data['latitude']), str(location_data['longitude']))
    chart = Chart(fdatetime, pos, hsys=const.HOUSES_PLACIDUS)

    table_data = [["Planet", "Sign", "Degree", "Nakshatra"]]
    for obj in const.LIST_SEVEN_PLANETS + [const.MOON, const.ASC, const.MC]:
        planet = chart.get(obj)
        sign = planet.sign
        degree = f"{int(planet.lon)}° {round((planet.lon % 1)*60)}'"
        nakshatra_index = int((planet.lon % 360) / (13 + 1/3))
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        nakshatra = nakshatras[nakshatra_index]
        table_data.append([obj, sign, degree, nakshatra])
    return table_data

# --- Helper: Generate PDF ---
def generate_pdf(table_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("Astro Planet Table", styles['Title'])
    elements.append(title)
    elements.append(Paragraph(" ", styles["Normal"]))

    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d0d0d0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- UI with Streamlit ---
st.title("🪐 Astro Chart Table Generator")

date_input = st.text_input("Enter Date (e.g. 7-8-2025)", "7-8-2025")
time_input = st.text_input("Enter Time (e.g. 9:15 am)", "9:15 am")
location_input = st.text_input("Enter Location (e.g. Mumbai India)", "Mumbai India")

if st.button("Generate Chart"):
    loc_data = get_location_data(location_input)
    if not loc_data:
        st.error("Location not found. Please enter a valid city name.")
    else:
        table = create_astro_table(date_input, time_input, loc_data)
        st.success("Astro Chart Generated!")
        st.table(table)

        pdf = generate_pdf(table)
        st.download_button(label="📥 Download as PDF", data=pdf, file_name="astro_chart.pdf", mime="application/pdf")
