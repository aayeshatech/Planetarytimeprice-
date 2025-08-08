import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import numpy as np
import math

# Set page config for a wider layout
st.set_page_config(layout="wide", page_title="Intraday Astro–Gann Swing Tool")

# Custom CSS for astro-themed styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1a237e;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #283593;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .info-box {
        background-color: #e8eaf6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #3f51b5;
        margin-bottom: 1rem;
    }
    .symbol-cmp {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1a237e;
        text-align: center;
        padding: 0.8rem;
        background-color: #c5cae9;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .data-table {
        font-size: 1.1rem !important;
    }
    .important-row {
        background-color: #4caf50 !important;
        font-weight: bold !important;
    }
    .current-transit-row {
        background-color: #ffeb3b !important;
        border: 2px solid #ff9800 !important;
        box-shadow: 0 0 10px rgba(255, 152, 0, 0.5) !important;
    }
    .both-row {
        background-color: #ff9800 !important;
        font-weight: bold !important;
        border: 2px solid #f44336 !important;
        box-shadow: 0 0 10px rgba(244, 67, 54, 0.5) !important;
    }
    .favorable-row {
        background-color: #c8e6c9 !important;
        border-left: 4px solid #4caf50 !important;
    }
    .negative-row {
        background-color: #ffcdd2 !important;
        border-left: 4px solid #f44336 !important;
    }
    .planet-icon {
        display: inline-block;
        margin-right: 5px;
    }
    .current-transit-indicator {
        position: relative;
        display: inline-block;
        padding: 0 5px;
    }
    .current-transit-indicator::after {
        content: "⚡";
        position: absolute;
        top: -5px;
        right: -10px;
        color: #ff9800;
        font-size: 1.2rem;
    }
    .transit-box {
        background-color: #f5f5f5;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .warning-message {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .error-message {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<div class="main-header">Intraday Astro–Gann Swing Tool</div>', unsafe_allow_html=True)

# Input fields in columns
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    date_input = st.date_input("Select Date", datetime.today())
    time_input = st.time_input("Select Time", datetime.now().time())
with col2:
    location_input = st.text_input("Enter Location (e.g., Mumbai, India)", "Mumbai, India")
    symbol = st.text_input("Symbol", "Nifty")
with col3:
    cmp = st.number_input("CMP (Current Market Price)", value=24574.0)
    market = st.radio("Select Market", ["Indian Market", "Global Market"])

# Font size control for the table
font_size = st.slider("Table Font Size", min_value=12, max_value=24, value=16, step=1)

# Background color picker for the intraday swing range box
box_bg_color = st.color_picker("Background Color for Intraday Swing Range Box", "#e8eaf6")

# Swing range multiplier to adjust for higher market fluctuations
swing_range_multiplier = st.slider("Swing Range Multiplier", min_value=0.5, max_value=3.0, value=1.0, step=0.1)

# Generate button
generate_report = st.button("Generate Report", key="generate_btn")

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
    if market == "Global Market":
        # For global market, show all times without adjustment
        return start_time, end_time
        
    if start_time.time() < market_start:
        start_time = datetime.combine(start_time.date(), market_start)
    if end_time.time() > market_end:
        end_time = datetime.combine(end_time.date(), market_end)
    
    # If the entire window is outside market hours, return None
    if start_time >= end_time:
        return None, None
    
    return start_time, end_time

# Function to determine if a planet's transit is favorable or negative
def get_transit_nature(planet, degree):
    # Define favorable and unfavorable degrees for each planet
    favorable_degrees = {
        "Sun": [(0, 30), (120, 150), (240, 270)],  # Aries, Leo, Sagittarius
        "Moon": [(60, 90), (150, 180), (270, 300)],  # Taurus, Cancer, Pisces
        "Mercury": [(60, 90), (180, 210), (300, 330)],  # Taurus, Virgo, Capricorn
        "Venus": [(30, 60), (150, 180), (270, 300)],  # Taurus, Libra, Pisces
        "Mars": [(0, 30), (90, 120), (240, 270)],  # Aries, Scorpio, Capricorn
        "Jupiter": [(0, 30), (120, 150), (240, 270)],  # Aries, Leo, Sagittarius
        "Saturn": [(60, 90), (210, 240), (300, 330)]  # Taurus, Libra, Aquarius
    }
    
    # Check if the planet's degree falls in any favorable range
    for start, end in favorable_degrees.get(planet, []):
        if start <= degree <= end:
            return "Favorable"
    
    # If not in favorable range, check for unfavorable ranges (opposite signs)
    unfavorable_degrees = {
        "Sun": [(90, 120), (210, 240), (330, 360)],  # Gemini, Aquarius, Pisces
        "Moon": [(0, 30), (120, 150), (210, 240)],  # Aries, Leo, Scorpio
        "Mercury": [(0, 30), (120, 150), (210, 240)],  # Aries, Leo, Scorpio
        "Venus": [(120, 150), (210, 240), (330, 360)],  # Leo, Scorpio, Pisces
        "Mars": [(60, 90), (180, 210), (300, 330)],  # Taurus, Virgo, Capricorn
        "Jupiter": [(90, 120), (210, 240), (330, 360)],  # Gemini, Scorpio, Pisces
        "Saturn": [(0, 30), (120, 150), (240, 270)]  # Aries, Leo, Sagittarius
    }
    
    for start, end in unfavorable_degrees.get(planet, []):
        if start <= degree <= end:
            return "Negative"
    
    # If neither favorable nor unfavorable, return neutral
    return "Neutral"

# Function to calculate Moon-Rahu and Moon-Ketu transit times
def calculate_moon_nodes_transit(dt, moon_degree):
    # Rahu and Ketu are always 180 degrees apart
    # We'll assume Rahu is at a fixed position and Ketu is opposite
    # In a real application, these would be calculated based on ephemeris data
    
    # For demonstration, let's place Rahu at 90 degrees and Ketu at 270 degrees
    rahu_degree = 90
    ketu_degree = 270
    
    # Calculate when Moon will be in aspect with Rahu and Ketu
    # We'll consider aspects at 0, 60, 90, 120, 180 degrees
    
    moon_speed = 0.5  # degrees per hour (approximate)
    
    # Calculate time for Moon-Rahu aspects
    moon_rahu_aspects = []
    for aspect in [0, 60, 90, 120, 180]:
        target_degree = (rahu_degree + aspect) % 360
        
        # Calculate the difference in degrees
        diff = (target_degree - moon_degree) % 360
        if diff > 180:
            diff -= 360
        
        # Calculate the time to reach the aspect
        hours_to_aspect = diff / moon_speed
        
        if hours_to_aspect > 0:  # Only future aspects
            aspect_time = dt + timedelta(hours=hours_to_aspect)
            moon_rahu_aspects.append({
                "aspect": f"Moon-Rahu {aspect}°",
                "time": aspect_time.strftime('%I:%M %p')
            })
    
    # Calculate time for Moon-Ketu aspects
    moon_ketu_aspects = []
    for aspect in [0, 60, 90, 120, 180]:
        target_degree = (ketu_degree + aspect) % 360
        
        # Calculate the difference in degrees
        diff = (target_degree - moon_degree) % 360
        if diff > 180:
            diff -= 360
        
        # Calculate the time to reach the aspect
        hours_to_aspect = diff / moon_speed
        
        if hours_to_aspect > 0:  # Only future aspects
            aspect_time = dt + timedelta(hours=hours_to_aspect)
            moon_ketu_aspects.append({
                "aspect": f"Moon-Ketu {aspect}°",
                "time": aspect_time.strftime('%I:%M %p')
            })
    
    return moon_rahu_aspects, moon_ketu_aspects

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

# Calculate Gann price levels based on planet's degree
def calculate_gann_levels(cmp, planet_degree, planet_name):
    # Gann's 360-degree circle divided into 12 parts (30 degrees each)
    # Each part corresponds to a zodiac sign with specific characteristics
    
    # Calculate the zodiac sign (0-11)
    zodiac_index = int(planet_degree / 30) % 12
    
    # Define volatility factors for each zodiac sign
    zodiac_volatility = {
        0: 1.2,   # Aries - high volatility
        1: 0.8,   # Taurus - low volatility
        2: 1.1,   # Gemini - medium-high volatility
        3: 0.9,   # Cancer - low-medium volatility
        4: 1.3,   # Leo - very high volatility
        5: 1.0,   # Virgo - medium volatility
        6: 1.0,   # Libra - medium volatility
        7: 1.1,   # Scorpio - medium-high volatility
        8: 0.7,   # Sagittarius - very low volatility
        9: 0.9,   # Capricorn - low-medium volatility
        10: 1.2,  # Aquarius - high volatility
        11: 0.8   # Pisces - low volatility
    }
    
    # Define planet-specific multipliers
    planet_multipliers = {
        "Sun": 1.0,
        "Moon": 0.8,
        "Mercury": 1.1,
        "Venus": 0.7,
        "Mars": 1.3,
        "Jupiter": 1.2,
        "Saturn": 0.9
    }
    
    # Calculate the degree within the zodiac sign (0-30)
    degree_in_sign = planet_degree % 30
    
    # Calculate the volatility factor based on zodiac sign and planet
    volatility_factor = zodiac_volatility[zodiac_index] * planet_multipliers[planet_name]
    
    # Adjust volatility based on position within the sign
    # Higher volatility at the beginning and end of signs (critical degrees)
    if degree_in_sign < 5 or degree_in_sign > 25:
        volatility_factor *= 1.2
    
    # Calculate the base range percentage
    base_range_percent = 0.01  # 1% base range
    
    # Apply the swing range multiplier to account for higher market fluctuations
    base_range_percent *= swing_range_multiplier
    
    # Apply volatility factor to get the actual range percentage
    range_percent = base_range_percent * volatility_factor
    
    # Calculate swing range
    range_size = cmp * range_percent
    swing_low = cmp - range_size
    swing_high = cmp + range_size
    
    # Calculate degree range (±3 degrees adjusted by volatility)
    degree_range = 3 * volatility_factor
    degree_low = (planet_degree - degree_range) % 360
    degree_high = (planet_degree + degree_range) % 360
    
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
    
    # If the selected time is outside market hours, adjust to the nearest market hour
    if market == "Indian Market":
        if dt.time() < market_start:
            center_time = datetime.combine(dt.date(), market_start)
        elif dt.time() > market_end:
            center_time = datetime.combine(dt.date(), market_end)
        else:
            center_time = dt
    else:
        center_time = dt
    
    start_time = center_time - timedelta(minutes=duration//2)
    end_time = center_time + timedelta(minutes=duration//2)
    
    return start_time, end_time

# Generate report only when button is clicked
if generate_report:
    # Check if the selected date is a weekend (for Indian Market)
    if market == "Indian Market" and date_input.weekday() >= 5:  # 5=Saturday, 6=Sunday
        st.markdown('<div class="error-message"><strong>Market Closed</strong><br>The selected date is a weekend. Indian Market is closed on Saturdays and Sundays. Please select a weekday.</div>', unsafe_allow_html=True)
        st.stop()
    
    # Check if the selected time is outside market hours (for Indian Market)
    if market == "Indian Market" and not is_within_market_hours(time_input):
        st.markdown(f'<div class="warning-message"><strong>Outside Market Hours</strong><br>The selected time is outside Indian Market hours ({market_start.strftime("%I:%M %p")} to {market_end.strftime("%I:%M %p")}). The report will show transits during market hours only.</div>', unsafe_allow_html=True)
    
    # Get planetary positions
    planetary_positions = get_planetary_positions(dt)
    
    # Get important planet for the day
    important_planet = get_important_planet(date_input)
    
    # Calculate Moon-Rahu and Moon-Ketu transits
    moon_degree = planetary_positions.get("Moon", 0)
    moon_rahu_aspects, moon_ketu_aspects = calculate_moon_nodes_transit(dt, moon_degree)
    
    # Prepare data for each planet
    results = []
    for planet, degree in planetary_positions.items():
        # Calculate Gann levels with planet-specific parameters
        swing_low, swing_high, degree_low, degree_high = calculate_gann_levels(cmp, degree, planet)
        
        start_time, end_time = calculate_timing(dt, planet)
        
        # Adjust timing to market hours
        adj_start_time, adj_end_time = adjust_timing_to_market(start_time, end_time)
        
        # Skip if outside market hours (only for Indian Market)
        if market == "Indian Market" and (adj_start_time is None or adj_end_time is None):
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
        
        # Check if current time is within this planet's transit window
        current_time = datetime.now().time()
        current_dt = datetime.combine(date_input, current_time)
        is_current_transit = adj_start_time <= current_dt <= adj_end_time
        
        # Determine transit nature (favorable/negative/neutral)
        transit_nature = get_transit_nature(planet, degree)
        
        results.append({
            "Symbol": symbol,
            "CMP": f"₹{cmp:.2f}",
            "Swing Low": f"₹{swing_low:.2f}",
            "Swing High": f"₹{swing_high:.2f}",
            "Degree Range": f"{degree_low:.2f}°–{degree_high:.2f}°",
            "Key Planet": planet_display,
            "Timing (IST)": timing_str,
            "Transit Nature": transit_nature,
            "Important": "Yes" if is_important else "No",
            "Current Transit": "Yes" if is_current_transit else "No"
        })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Check if DataFrame is empty
    if df.empty:
        if market == "Indian Market":
            st.markdown('<div class="error-message"><strong>No Planetary Transits During Market Hours</strong><br>There are no planetary transits within market hours for the selected date. This could be due to:<ul><li>The selected date is a market holiday</li><li>All planetary transits fall outside market hours</li></ul>Please try a different date.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message"><strong>No Planetary Transits Found</strong><br>No planetary transits were found for the selected date and time. Please try a different date or time.</div>', unsafe_allow_html=True)
        st.stop()  # Stop execution here
    
    # Display Symbol and CMP above the table
    st.markdown(f'<div class="symbol-cmp">Symbol: {symbol} | CMP: ₹{cmp:.2f}</div>', unsafe_allow_html=True)
    
    # Display the important planet information
    st.markdown(f'<div class="info-box"><strong>Important Planet for Trading: {important_planet}</strong><br>The ruling planet for {date_input.strftime("%A")} is {important_planet}. Pay special attention to its transit and levels during the trading session.</div>', unsafe_allow_html=True)
    
    # Display market hours
    st.markdown(f'<div class="sub-header">Market Hours: {market_start.strftime("%I:%M %p")} to {market_end.strftime("%I:%M %p")}</div>', unsafe_allow_html=True)
    
    # Display Moon-Rahu and Moon-Ketu transits
    st.markdown('<div class="sub-header">Moon-Nodes Transit</div>', unsafe_allow_html=True)
    
    # Create two columns for Moon-Rahu and Moon-Ketu transits
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="transit-box"><strong>Moon-Rahu Transit</strong></div>', unsafe_allow_html=True)
        if moon_rahu_aspects:
            for aspect in moon_rahu_aspects:
                st.markdown(f'<div class="transit-box">{aspect["aspect"]}: {aspect["time"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="transit-box">No Moon-Rahu aspects today</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="transit-box"><strong>Moon-Ketu Transit</strong></div>', unsafe_allow_html=True)
        if moon_ketu_aspects:
            for aspect in moon_ketu_aspects:
                st.markdown(f'<div class="transit-box">{aspect["aspect"]}: {aspect["time"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="transit-box">No Moon-Ketu aspects today</div>', unsafe_allow_html=True)
    
    # Display the table with highlighting
    st.markdown('<div class="sub-header">Intraday Swing Range</div>', unsafe_allow_html=True)
    
    # Create a copy of the dataframe for styling
    styled_df = df.copy()
    
    # Apply styling using pandas Styler
    def highlight_rows(row):
        styles = [''] * len(row)
        
        # Highlight based on transit nature
        if row['Transit Nature'] == 'Favorable':
            styles = ['background-color: #c8e6c9; border-left: 4px solid #4caf50'] * len(row)
        elif row['Transit Nature'] == 'Negative':
            styles = ['background-color: #ffcdd2; border-left: 4px solid #f44336'] * len(row)
        
        # Highlight based on importance and current transit
        if row['Important'] == 'Yes' and row['Current Transit'] == 'Yes':
            styles = ['background-color: orange; font-weight: bold; border: 2px solid #f44336; box-shadow: 0 0 10px rgba(244, 67, 54, 0.5)'] * len(row)
        elif row['Important'] == 'Yes':
            if row['Transit Nature'] == 'Neutral':
                styles = ['background-color: lightgreen; font-weight: bold'] * len(row)
        elif row['Current Transit'] == 'Yes':
            if row['Transit Nature'] == 'Neutral':
                styles = ['background-color: yellow; border: 2px solid #ff9800; box-shadow: 0 0 10px rgba(255, 152, 0, 0.5)'] * len(row)
        
        return styles
    
    # Apply the styling
    styled_df = styled_df.style.apply(highlight_rows, axis=1)
    styled_df = styled_df.set_properties(**{'font-size': f'{font_size}px'})
    
    # Display the styled dataframe
    st.dataframe(styled_df, use_container_width=True)
    
    # --- PDF Generation ---
    def generate_pdf(dataframe):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=12
        )
        elements.append(Paragraph("Intraday Astro–Gann Swing Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Symbol and CMP
        symbol_style = ParagraphStyle(
            name='Symbol',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=12
        )
        elements.append(Paragraph(f"Symbol: {symbol} | CMP: ₹{cmp:.2f}", symbol_style))
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
        
        # Moon-Nodes Transit
        elements.append(Paragraph("Moon-Nodes Transit", styles['Heading2']))
        elements.append(Spacer(1, 6))
        
        # Moon-Rahu Transit
        elements.append(Paragraph("Moon-Rahu Transit", styles['Heading3']))
        if moon_rahu_aspects:
            for aspect in moon_rahu_aspects:
                elements.append(Paragraph(f"{aspect['aspect']}: {aspect['time']}", styles['Normal']))
        else:
            elements.append(Paragraph("No Moon-Rahu aspects today", styles['Normal']))
        elements.append(Spacer(1, 6))
        
        # Moon-Ketu Transit
        elements.append(Paragraph("Moon-Ketu Transit", styles['Heading3']))
        if moon_ketu_aspects:
            for aspect in moon_ketu_aspects:
                elements.append(Paragraph(f"{aspect['aspect']}: {aspect['time']}", styles['Normal']))
        else:
            elements.append(Paragraph("No Moon-Ketu aspects today", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Location and time
        dt_str = dt.strftime('%d %B %Y, %I:%M %p')
        elements.append(Paragraph(f"Date & Time: {dt_str}", styles['Normal']))
        elements.append(Paragraph(f"Location: {location_input}", styles['Normal']))
        elements.append(Paragraph(f"Market: {market} ({market_start.strftime('%I:%M %p')} to {market_end.strftime('%I:%M %p')})", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Table content - only if dataframe is not empty
        if not dataframe.empty:
            table_data = [list(dataframe.columns)] + dataframe.values.tolist()
            
            # Define column widths for better layout
            colWidths = [
                1.0 * inch,  # Symbol
                0.8 * inch,  # CMP
                1.0 * inch,  # Swing Low
                1.0 * inch,  # Swing High
                1.2 * inch,  # Degree Range
                1.5 * inch,  # Key Planet
                1.5 * inch,  # Timing
                1.0 * inch,  # Transit Nature
                0.8 * inch,  # Important
                0.8 * inch   # Current Transit
            ]
            
            table = Table(table_data, colWidths=colWidths)
            
            # Build style commands
            style_commands = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), font_size/2),  # Convert to points (1px ≈ 0.75pt)
                # First, set all rows to white
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ]
            
            # Highlight rows based on importance, current transit, and transit nature
            for i, row in enumerate(table_data[1:], start=1):
                important = row[-2] == 'Yes'  # Second last column
                current_transit = row[-1] == 'Yes'  # Last column
                transit_nature = row[-3]  # Third last column
                
                if important and current_transit:
                    style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.orange))
                    style_commands.append(('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold'))
                    style_commands.append(('BOX', (0, i), (-1, i), 2, colors.red))
                elif current_transit:
                    style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.yellow))
                    style_commands.append(('BOX', (0, i), (-1, i), 2, colors.orange))
                elif important:
                    style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.lightgreen))
                    style_commands.append(('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold'))
                elif transit_nature == 'Favorable':
                    style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.lightgreen))
                    style_commands.append(('LINEBEFORE', (0, i), (-1, i), 4, colors.green))
                elif transit_nature == 'Negative':
                    style_commands.append(('BACKGROUND', (0, i), (-1, i), colors.pink))
                    style_commands.append(('LINEBEFORE', (0, i), (-1, i), 4, colors.red))
            
            table.setStyle(TableStyle(style_commands))
            elements.append(table)
        else:
            # Add a message when there's no data
            no_data_style = ParagraphStyle(
                name='NoData',
                parent=styles['Normal'],
                textColor=colors.red,
                alignment=1  # Center alignment
            )
            elements.append(Paragraph("No planetary transits within market hours for the selected date and time.", no_data_style))
        
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
    
    # Apply custom background color to the intraday swing range box
    st.markdown(f"""
    <style>
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlock"] > div > div > div > .dataframe) {{
            background-color: {box_bg_color};
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #3f51b5;
            margin-bottom: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)
