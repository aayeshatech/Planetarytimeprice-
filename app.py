import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import numpy as np

# Title
st.title("Intraday Astro–Gann Swing Tool")

# Input fields
col1, col2 = st.columns(2)
with col1:
    date_input = st.date_input("Select Date", datetime.today())
    time_input = st.time_input("Select Time", datetime.now().time())
with col2:
    location_input = st.text_input("Enter Location (e.g., Mumbai, India)", "Mumbai, India")
    symbol = st.text_input("Symbol", "Nifty")
    cmp = st.number_input("CMP (Current Market Price)", value=24574.0)

# Combine date and time
dt = datetime.combine(date_input, time_input)

# Mock planetary positions calculation (in a real app, use an ephemeris library)
def get_planetary_positions(dt):
    # Simplified calculation for demonstration
    base_positions = {
        "Sun": 120.54,
        "Moon": 183.77,
        "Mercury": 45.32,
        "Venus": 210.65,
        "Mars": 95.78,
        "Jupiter": 310.22,
        "Saturn": 275.43
    }
    
    # Add some variation based on time
    time_factor = (dt.hour * 60 + dt.minute) / (24 * 60)
    positions = {}
    for planet, base_pos in base_positions.items():
        # Simulate planetary movement
        movement = {
            "Sun": 0.04,  # degrees per hour
            "Moon": 0.5,
            "Mercury": 0.3,
            "Venus": 0.2,
            "Mars": 0.1,
            "Jupiter": 0.05,
            "Saturn": 0.03
        }
        positions[planet] = (base_pos + movement[planet] * dt.hour) % 360
    
    return positions

# Get nakshatra based on moon's position
def get_nakshatra(degree):
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    index = int(degree / (360/27)) % 27
    return nakshatras[index]

# Calculate Gann price levels
def calculate_gann_levels(cmp, planet_degree):
    # Simplified Gann calculation for demonstration
    base_price = cmp - (cmp % 90)  # Round down to nearest 90
    degree_factor = planet_degree / 360
    
    # Calculate swing range
    range_size = cmp * 0.012  # ~1.2% range
    swing_low = cmp - range_size
    swing_high = cmp + range_size
    
    # Degree range based on planet position
    degree_low = (planet_degree - 3) % 360
    degree_high = (planet_degree + 3) % 360
    
    return swing_low, swing_high, degree_low, degree_high

# Calculate timing window
def calculate_timing(dt, planet):
    # Simplified timing calculation
    base_duration = {
        "Sun": 30,    # minutes
        "Moon": 90,
        "Mercury": 45,
        "Venus": 60,
        "Mars": 75,
        "Jupiter": 120,
        "Saturn": 150
    }
    
    duration = base_duration.get(planet, 60)
    start_time = dt - timedelta(minutes=duration//2)
    end_time = dt + timedelta(minutes=duration//2)
    
    return start_time, end_time

# Get planetary positions
planetary_positions = get_planetary_positions(dt)

# Prepare data for each planet
results = []
for planet, degree in planetary_positions.items():
    swing_low, swing_high, degree_low, degree_high = calculate_gann_levels(cmp, degree)
    start_time, end_time = calculate_timing(dt, planet)
    
    # Format timing
    timing_str = f"{start_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}"
    
    # Get nakshatra for Moon
    if planet == "Moon":
        nakshatra = get_nakshatra(degree)
        planet_display = f"Moon in {nakshatra}"
    else:
        planet_display = planet
    
    results.append({
        "Symbol": symbol,
        "CMP": f"₹{cmp:.2f}",
        "Swing Low": f"₹{swing_low:.2f}",
        "Swing High": f"₹{swing_high:.2f}",
        "Degree Range": f"{degree_low:.2f}°–{degree_high:.2f}°",
        "Key Planet": planet_display,
        "Timing (IST)": timing_str
    })

# Create DataFrame
df = pd.DataFrame(results)

# Display the table
st.subheader("Intraday Swing Range")
st.dataframe(df)

# --- PDF Generation ---
def generate_pdf(dataframe):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("Intraday Astro–Gann Swing Report", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Location and time
    dt_str = dt.strftime('%d %B %Y, %I:%M %p')
    elements.append(Paragraph(f"Date & Time: {dt_str}", styles['Normal']))
    elements.append(Paragraph(f"Location: {location_input}", styles['Normal']))
    elements.append(Paragraph(f"Symbol: {symbol}", styles['Normal']))
    elements.append(Paragraph(f"CMP: ₹{cmp:.2f}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Table content
    table_data = [list(dataframe.columns)] + dataframe.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Download as PDF
pdf_buffer = generate_pdf(df)
st.download_button(
    label="Download PDF",
    data=pdf_buffer,
    file_name=f"astro_gann_report_{date_input.strftime('%Y-%m-%d')}.pdf",
    mime="application/pdf"
)

# Download as Excel
excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False, engine='openpyxl')
excel_buffer.seek(0)
st.download_button(
    label="Download Excel",
    data=excel_buffer,
    file_name=f"astro_gann_report_{date_input.strftime('%Y-%m-%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
