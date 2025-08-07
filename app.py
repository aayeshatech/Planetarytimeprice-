import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

# Market selection
market = st.radio("Select Market", ["Indian Market", "Global Market"])

# Generate button
generate_report = st.button("Generate Report")

# Define market hours
if market == "Indian Market":
    market_start = datetime.strptime("09:15", "%H:%M").time()
    market_end = datetime.strptime("15:15", "%H:%M").time()
else:
    market_start = datetime.strptime("05:00", "%H:%M").time()
    market_end = datetime.strptime("23:35", "%H:%M").time()

# Function to determine the important planet for the day
def get_important_planet(date):
    day_of_week = date.weekday()  # Monday is 0, Sunday is 6
    day_rulers = {
        0: "Moon",      # Monday
        1: "Mars",      # Tuesday
        2: "Mercury",   # Wednesday
        3: "Jupiter",   # Thursday
        4: "Venus",     # Friday
        5: "Saturn",    # Saturday
        6: "Sun"        # Sunday
    }
    return day_rulers.get(day_of_week, "Moon")

# Function to check if time is within market hours
def is_within_market_hours(time):
    return market_start <= time <= market_end

# Function to adjust timing to market hours
def adjust_timing_to_market(start_time, end_time):
    if start_time.time() < market_start:
        start_time = datetime.combine(start_time.date(), market_start)
    if end_time.time() > market_end:
        end_time = datetime.combine(end_time.date(), market_end)
    
    # If the entire window is outside market hours, return None
    if start_time >= end_time:
        return None, None
    
    return start_time, end_time

# Combine date and time
dt = datetime.combine(date_input, time_input)

# Mock planetary positions calculation
def get_planetary_positions(dt):
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
            "Sun": 0.04,
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
    base_price = cmp - (cmp % 90)
    degree_factor = planet_degree / 360
    
    # Calculate swing range
    range_size = cmp * 0.012
    swing_low = cmp - range_size
    swing_high = cmp + range_size
    
    # Degree range based on planet position
    degree_low = (planet_degree - 3) % 360
    degree_high = (planet_degree + 3) % 360
    
    return swing_low, swing_high, degree_low, degree_high

# Calculate timing window
def calculate_timing(dt, planet):
    base_duration = {
        "Sun": 30,
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

# Generate report only when button is clicked
if generate_report:
    # Get planetary positions
    planetary_positions = get_planetary_positions(dt)
    
    # Get important planet for the day
    important_planet = get_important_planet(date_input)
    
    # Prepare data for each planet
    results = []
    for planet, degree in planetary_positions.items():
        swing_low, swing_high, degree_low, degree_high = calculate_gann_levels(cmp, degree)
        start_time, end_time = calculate_timing(dt, planet)
        
        # Adjust timing to market hours
        adj_start_time, adj_end_time = adjust_timing_to_market(start_time, end_time)
        
        # Skip if outside market hours
        if adj_start_time is None or adj_end_time is None:
            continue
            
        # Format timing
        timing_str = f"{adj_start_time.strftime('%I:%M %p')} – {adj_end_time.strftime('%I:%M %p')}"
        
        # Get nakshatra for Moon
        if planet == "Moon":
            nakshatra = get_nakshatra(degree)
            planet_display = f"Moon in {nakshatra}"
        else:
            planet_display = planet
        
        # Check if this is the important planet
        is_important = (planet == important_planet)
        
        results.append({
            "Symbol": symbol,
            "CMP": f"₹{cmp:.2f}",
            "Swing Low": f"₹{swing_low:.2f}",
            "Swing High": f"₹{swing_high:.2f}",
            "Degree Range": f"{degree_low:.2f}°–{degree_high:.2f}°",
            "Key Planet": planet_display,
            "Timing (IST)": timing_str,
            "Important": "Yes" if is_important else "No"
        })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Display the important planet information
    st.subheader(f"Important Planet for Trading: {important_planet}")
    st.write(f"The ruling planet for {date_input.strftime('%A')} is {important_planet}. "
             f"Pay special attention to its transit and levels during the trading session.")
    
    # Display market hours
    st.subheader(f"Market Hours: {market_start.strftime('%I:%M %p')} to {market_end.strftime('%I:%M %p')}")
    
    # Display the table
    st.subheader("Intraday Swing Range")
    st.dataframe(df.style.apply(lambda x: ['background: lightgreen' if x.Important == 'Yes' else '' for i in x], axis=1))
    
    # --- PDF Generation ---
    def generate_pdf(dataframe):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph("Intraday Astro–Gann Swing Report", styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Important planet
        important_style = ParagraphStyle(
            name='Important',
            parent=styles['Heading2'],
            textColor=colors.red,
            spaceAfter=12
        )
        elements.append(Paragraph(f"Important Planet for Trading: {important_planet}", important_style))
        elements.append(Paragraph(f"The ruling planet for {date_input.strftime('%A')} is {important_planet}. "
                                f"Pay special attention to its transit and levels during the trading session.", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Location and time
        dt_str = dt.strftime('%d %B %Y, %I:%M %p')
        elements.append(Paragraph(f"Date & Time: {dt_str}", styles['Normal']))
        elements.append(Paragraph(f"Location: {location_input}", styles['Normal']))
        elements.append(Paragraph(f"Symbol: {symbol}", styles['Normal']))
        elements.append(Paragraph(f"CMP: ₹{cmp:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Market: {market} ({market_start.strftime('%I:%M %p')} to {market_end.strftime('%I:%M %p')})", styles['Normal']))
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
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            # Highlight important planet rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), lambda i,j: colors.lightgreen if table_data[i+1][-1] == 'Yes' else colors.white)
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
