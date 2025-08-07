import streamlit as st
from datetime import datetime
from pytz import timezone
import swisseph as swe
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# Load ephemeris
swe.set_ephe_path("/usr/share/ephe")  # You may need to adjust this

def price_to_degree(price, base=360):
    return (price % base)

def degree_to_price(degree, base=360):
    return degree + (base * (int(price) // base))

def get_planet_positions(jd):
    planets = {
        'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
        'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN, 'Rahu (Mean)': swe.MEAN_NODE, 'Ketu (Mean)': swe.MEAN_NODE
    }

    positions = []
    for name, pid in planets.items():
        lon, _ = swe.calc_ut(jd, pid)
        if name == 'Ketu (Mean)':
            lon = (lon + 180) % 360
        positions.append({
            'Planet': name,
            'Degree': round(lon, 2)
        })

    return pd.DataFrame(positions)

def create_pdf(dataframe):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    style = getSampleStyleSheet()
    title = Paragraph("Planetary Degree to Price Mapping", style['Title'])
    elements.append(title)
    table_data = [list(dataframe.columns)] + dataframe.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---- Streamlit App ----
st.title("📈 Intraday Astro-Gann Price Degree Calculator")

symbol = st.text_input("Enter Symbol (e.g., NIFTY)", value="NIFTY")
price = st.number_input("Enter CMP Price", value=22200.0)
date_input = st.date_input("Select Date", value=datetime.now().date())
time_input = st.time_input("Select Time (IST)", value=datetime.now().time())
location = st.text_input("Enter Location (City)", value="Mumbai")

if st.button("Calculate Astro Mapping"):
    # Convert to UTC datetime
    dt = datetime.combine(date_input, time_input)
    tz = timezone("Asia/Kolkata")
    dt_local = tz.localize(dt)
    dt_utc = dt_local.astimezone(timezone("UTC"))
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60.0)

    df = get_planet_positions(jd)
    df['Mapped Price'] = df['Degree'].apply(lambda d: round(degree_to_price(d, base=360), 2))
    df['Price Degree'] = df['Degree'].apply(lambda d: round(d, 2))

    st.subheader("🪐 Planetary Degrees and Price Mapping")
    st.dataframe(df)

    # PDF download
    pdf_data = create_pdf(df)
    st.download_button("📄 Download PDF", data=pdf_data, file_name=f"{symbol}_astro_mapping.pdf", mime="application/pdf")

