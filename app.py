import streamlit as st
import swisseph as swe
import datetime
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# Set ephemeris path
swe.set_ephe_path('.')

# Planet names mapping
planet_names = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MERCURY: "Mercury",
    swe.VENUS: "Venus",
    swe.MARS: "Mars",
    swe.JUPITER: "Jupiter",
    swe.SATURN: "Saturn",
    swe.URANUS: "Uranus",
    swe.NEPTUNE: "Neptune",
    swe.PLUTO: "Pluto"
}

# Function to get planetary positions
def get_planet_positions(jd, cmp):
    data = []
    price_per_degree = cmp / 360
    for planet in planet_names:
        lon, _ = swe.calc_ut(jd, planet)
        degree = round(lon[0], 2)
        price_at_degree = round(price_per_degree * degree, 2)
        data.append({
            "Planet": planet_names[planet],
            "Degree": degree,
            "Price (CMP×Degree/360)": price_at_degree
        })
    return pd.DataFrame(data)

# Convert to PDF
def generate_pdf(dataframe):
    filename = "/mnt/data/Planetary_Price_Table.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    style = getSampleStyleSheet()

    title = Paragraph("Planetary Price Degree Table", style['Title'])
    elements.append(title)
    table_data = [list(dataframe.columns)] + dataframe.values.tolist()

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER')
    ]))

    elements.append(table)
    doc.build(elements)
    return filename

# Streamlit UI
st.title("🪐 Planetary Degree vs Price Calculator")

symbol = st.text_input("Enter Symbol (e.g., NIFTY, GOLD, BTC):", "NIFTY")
cmp = st.number_input("Enter CMP (Current Market Price):", min_value=0.0, value=22000.0)

col1, col2 = st.columns(2)
with col1:
    date_input = st.date_input("Select Date", datetime.date.today())
with col2:
    time_input = st.time_input("Select Time", datetime.datetime.now().time())

# Calculate Julian Day
dt = datetime.datetime.combine(date_input, time_input)
jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

if st.button("🧮 Calculate Planetary Price Table"):
    df = get_planet_positions(jd, cmp)
    st.dataframe(df)

    # Generate PDF
    pdf_path = generate_pdf(df)
    with open(pdf_path, "rb") as file:
        btn = st.download_button(
            label="📄 Download PDF",
            data=file,
            file_name="Planetary_Price_Table.pdf",
            mime="application/pdf"
        )
