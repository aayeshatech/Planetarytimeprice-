import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime
import pytz

# ------------------ Input UI -------------------
st.title("🪐 Astro Intraday Levels Generator")

symbol = st.text_input("Symbol", value="NIFTY")
cmp = st.number_input("CMP (Current Market Price)", value=24344.0)
input_datetime = st.text_input("Date & Time (e.g., 7-8-2025 9:15 am)", value="7-8-2025 9:15 am")
location = st.text_input("Location (City, Country)", value="Mumbai, India")

# ------------------ Parse datetime -------------------
try:
    local = pytz.timezone("Asia/Kolkata")
    dt = datetime.strptime(input_datetime, "%d-%m-%Y %I:%M %p")
    dt = local.localize(dt)
except:
    st.error("❌ Invalid date format. Use dd-mm-yyyy hh:mm am/pm format.")
    st.stop()

# ------------------ Astro Engine -------------------
ts = load.timescale()
t = ts.from_datetime(dt)
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

# ------------------ Observer's Location -------------------
topos = Topos(latitude_degrees=18.975, longitude_degrees=72.825833)  # Mumbai

# ------------------ Compute Astro Levels -------------------
st.subheader(f"🧮 Astro Intraday Levels for {symbol.upper()} at {input_datetime} ({location})")

astro_levels = []
for name, body in planets.items():
    astrometric = (eph['earth'] + topos).at(t).observe(body).apparent()
    lon, lat, distance = astrometric.ecliptic_latlon()
    deg = lon.degrees

    # Intraday Price Levels (Gann-style)
    upper = cmp + (deg * cmp / 360)
    lower = cmp - (deg * cmp / 360)
    astro_levels.append((name, round(deg, 2), round(upper, 2), round(lower, 2)))

# ------------------ Display Table -------------------
import pandas as pd

df = pd.DataFrame(astro_levels, columns=["Planet", "Degree", "Upper Level", "Lower Level"])
st.dataframe(df)

# ------------------ Option to Download -------------------
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

if st.button("📥 Download PDF"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Astro Intraday Levels for {symbol.upper()}", styles['Title']))
    elements.append(Paragraph(f"Date & Time: {input_datetime}", styles['Normal']))
    elements.append(Paragraph(f"Location: {location}", styles['Normal']))
    elements.append(Paragraph(f"CMP: {cmp}", styles['Normal']))

    data = [["Planet", "Degree", "Upper Level", "Lower Level"]] + astro_levels
    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    st.download_button(label="📄 Download PDF", data=buffer.getvalue(), file_name=f"{symbol}_astro_levels.pdf", mime="application/pdf")

