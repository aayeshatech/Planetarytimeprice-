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
st.set_page_config(
    layout="wide", 
    page_title="Intraday Astro-Gann Swing Tool",
    page_icon="🌟",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern astro-themed styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-dark: #0a0e27;
        --primary-blue: #1a237e;
        --secondary-blue: #283593;
        --accent-purple: #3f51b5;
        --light-blue: #e8eaf6;
        --card-bg: #c5cae9;
        --gold: #ffd700;
        --silver: #c0c0c0;
        --success: #4caf50;
        --error: #f44336;
        --warning: #ff9800;
        --gradient-cosmic: linear-gradient(135deg, #0a0e27 0%, #1a237e 50%, #283593 100%);
        --gradient-card: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        --shadow-primary: 0 8px 32px rgba(26, 35, 126, 0.2);
        --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.1);
        --border-radius: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Global Styles */
    .stApp {
        background: var(--gradient-cosmic);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(63, 81, 181, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(26, 35, 126, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }

    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #ffd700, #ffffff, #c0c0c0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: white;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Planet Icons */
    .planet-icons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }

    .planet-icon {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        transition: var(--transition);
        cursor: pointer;
        box-shadow: var(--shadow-card);
    }

    .planet-icon:hover {
        transform: translateY(-3px) scale(1.1);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }

    .planet-sun { background: linear-gradient(45deg, #ff6b35, #ffd700); }
    .planet-moon { background: linear-gradient(45deg, #c0c0c0, #f8f8ff); color: #333; }
    .planet-mercury { background: linear-gradient(45deg, #87ceeb, #4682b4); }
    .planet-venus { background: linear-gradient(45deg, #ff69b4, #ffc0cb); }
    .planet-mars { background: linear-gradient(45deg, #dc143c, #ff4500); }
    .planet-jupiter { background: linear-gradient(45deg, #daa520, #ff8c00); }
    .planet-saturn { background: linear-gradient(45deg, #2f4f4f, #708090); }

    /* Card Styles */
    .info-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: var(--border-radius);
        border-left: 5px solid var(--gold);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-primary);
        backdrop-filter: blur(10px);
    }
    
    .symbol-cmp {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        text-align: center;
        padding: 1.5rem;
        background: var(--gradient-cosmic);
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-primary);
    }

    .market-status {
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-left: 5px solid var(--gold);
        box-shadow: var(--shadow-card);
    }

    .important-planet {
        background: linear-gradient(135deg, #ffd700, #ffecb3);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-card);
        border: 2px solid var(--gold);
    }

    .important-planet h2 {
        color: var(--primary-dark);
        margin-bottom: 1rem;
        font-size: 1.8rem;
        font-weight: 600;
    }

    /* Transit Cards */
    .transit-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(63, 81, 181, 0.2);
        box-shadow: var(--shadow-card);
        transition: var(--transition);
    }

    .transit-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26, 35, 126, 0.15);
    }

    .transit-box h4 {
        color: var(--primary-blue);
        margin-bottom: 1rem;
        font-weight: 600;
    }

    /* Table Styles */
    .dataframe {
        border-radius: var(--border-radius) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-primary) !important;
        border: none !important;
    }

    .dataframe thead tr th {
        background: var(--gradient-cosmic) !important;
        color: white !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        padding: 1rem !important;
    }

    .dataframe tbody tr td {
        padding: 1rem !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
        background: white !important;
    }

    .dataframe tbody tr:hover td {
        background: rgba(63, 81, 181, 0.02) !important;
    }

    /* Row Highlighting */
    .favorable-row {
        background-color: rgba(76, 175, 80, 0.1) !important;
        border-left: 4px solid var(--success) !important;
    }

    .negative-row {
        background-color: rgba(244, 67, 54, 0.1) !important;
        border-left: 4px solid var(--error) !important;
    }

    .important-row {
        background-color: rgba(255, 215, 0, 0.2) !important;
        font-weight: 600 !important;
        border-left: 4px solid var(--gold) !important;
    }

    .current-transit-row {
        background-color: rgba(255, 152, 0, 0.2) !important;
        border: 2px solid var(--warning) !important;
        position: relative !important;
    }

    .both-row {
        background-color: var(--warning) !important;
        font-weight: 600 !important;
        border: 2px solid var(--error) !important;
        box-shadow: 0 0 10px rgba(244, 67, 54, 0.5) !important;
    }

    /* Alert Messages */
    .warning-message {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border-left: 5px solid #ffc107;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-card);
    }

    .error-message {
        background: linear-gradient(135deg, #f8d7da, #fab1a0);
        border-left: 5px solid #dc3545;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-card);
    }

    .success-message {
        background: linear-gradient(135deg, #d1e7dd, #a8e6cf);
        border-left: 5px solid #198754;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-card);
    }

    /* Sidebar Styles */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Button Styles */
    .stButton > button {
        background: var(--gradient-cosmic) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-card) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(26, 35, 126, 0.3) !important;
    }

    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid var(--accent-purple) !important;
        color: var(--accent-purple) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: var(--transition) !important;
    }

    .stDownloadButton > button:hover {
        background: var(--accent-purple) !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }

    /* Input Styles */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid rgba(63, 81, 181, 0.2) !important;
        transition: var(--transition) !important;
    }

    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTimeInput > div > div > input:focus {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 0 3px rgba(63, 81, 181, 0.1) !important;
    }

    /* Slider Styles */
    .stSlider > div > div > div {
        background: var(--gradient-cosmic) !important;
    }

    /* Hide Streamlit branding */
    .css-1rs6os.edgvbvh3,
    .css-10trblm.e16nr0p30,
    #MainMenu,
    footer,
    header {
        visibility: hidden !important;
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .planet-icon {
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
        }
        
        .symbol-cmp {
            font-size: 1.4rem;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Title with planet icons
st.markdown("""
<div class="main-header">🌟 Intraday Astro–Gann Swing Tool 🌟</div>
<div class="planet-icons">
    <div class="planet-icon planet-sun" title="Sun">☉</div>
    <div class="planet-icon planet-moon" title="Moon">☽</div>
    <div class="planet-icon planet-mercury" title="Mercury">☿</div>
    <div class="planet-icon planet-venus" title="Venus">♀</div>
    <div class="planet-icon planet-mars" title="Mars">♂</div>
    <div class="planet-icon planet-jupiter" title="Jupiter">♃</div>
    <div class="planet-icon planet-saturn" title="Saturn">♄</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.markdown('<h2 style="color: var(--primary-blue); text-align: center;">⚙️ Control Panel</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📅 Date & Time Settings")
    date_input = st.date_input("Select Date", datetime.today())
    time_input = st.time_input("Select Time", datetime.now().time())
    location_input = st.text_input("Enter Location", "Mumbai, India")
    
    st.markdown("### 📈 Market Settings")
    symbol = st.text_input("Symbol", "Nifty")
    cmp = st.number_input("CMP (Current Market Price)", value=24574.0)
    market = st.radio("Select Market", ["Indian Market", "Global Market"])
    
    st.markdown("### 🔧 Advanced Settings")
    font_size = st.slider("Table Font Size", min_value=12, max_value=24, value=16, step=1)
    box_bg_color = st.color_picker("Background Color for Tables", "#e8eaf6")
    swing_range_multiplier = st.slider("Swing Range Multiplier", min_value=0.5, max_value=3.0, value=1.0, step=0.1)

# Generate button
generate_report = st.button("🔮 Generate Astro-Gann Report", use_container_width=True)

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
        return start_time, end_time
        
    if start_time.time() < market_start:
        start_time = datetime.combine(start_time.date(), market_start)
    if end_time.time() > market_end:
        end_time = datetime.combine(end_time.date(), market_end)
    
    if start_time >= end_time:
        return None, None
    
    return start_time, end_time

# Function to determine if a planet's transit is favorable or negative
def get_transit_nature(planet, degree):
    favorable_degrees = {
        "Sun": [(0, 30), (120, 150), (240, 270)],
        "Moon": [(60, 90), (150, 180), (270, 300)],
        "Mercury": [(60, 90), (180, 210), (300, 330)],
        "Venus": [(30, 60), (150, 180), (270, 300)],
        "Mars": [(0, 30), (90, 120), (240, 270)],
        "Jupiter": [(0, 30), (120, 150), (240, 270)],
        "Saturn": [(60, 90), (210, 240), (300, 330)]
    }
    
    for start, end in favorable_degrees.get(planet, []):
        if start <= degree <= end:
            return "Favorable"
    
    unfavorable_degrees = {
        "Sun": [(90, 120), (210, 240), (330, 360)],
        "Moon": [(0, 30), (120, 150), (210, 240)],
        "Mercury": [(0, 30), (120, 150), (210, 240)],
        "Venus": [(120, 150), (210, 240), (330, 360)],
        "Mars": [(60, 90), (180, 210), (300, 330)],
        "Jupiter": [(90, 120), (210, 240), (330, 360)],
        "Saturn": [(0, 30), (120, 150), (240, 270)]
    }
    
    for start, end in unfavorable_degrees.get(planet, []):
        if start <= degree <= end:
            return "Negative"
    
    return "Neutral"

# Function to calculate Moon-Rahu and Moon-Ketu transit times
def calculate_moon_nodes_transit(dt, moon_degree):
    rahu_degree = 90
    ketu_degree = 270
    moon_speed = 0.5
    
    moon_rahu_aspects = []
    for aspect in [0, 60, 90, 120, 180]:
        target_degree = (rahu_degree + aspect) % 360
        diff = (target_degree - moon_degree) % 360
        if diff > 180:
            diff -= 360
        
        hours_to_aspect = diff / moon_speed
        
        if hours_to_aspect > 0:
            aspect_time = dt + timedelta(hours=hours_to_aspect)
            moon_rahu_aspects.append({
                "aspect": f"Moon-Rahu {aspect}°",
                "time": aspect_time.strftime('%I:%M %p')
            })
    
    moon_ketu_aspects = []
    for aspect in [0, 60, 90, 120, 180]:
        target_degree = (ketu_degree + aspect) % 360
        diff = (target_degree - moon_degree) % 360
        if diff > 180:
            diff -= 360
        
        hours_to_aspect = diff / moon_speed
        
        if hours_to_aspect > 0:
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
    
    time_factor = (dt.hour * 60 + dt.minute) / (24 * 60)
    positions = {}
    for planet, base_pos in base_positions.items():
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
    zodiac_index = int(planet_degree / 30) % 12
    
    zodiac_volatility = {
        0: 1.2, 1: 0.8, 2: 1.1, 3: 0.9, 4: 1.3, 5: 1.0,
        6: 1.0, 7: 1.1, 8: 0.7, 9: 0.9, 10: 1.2, 11: 0.8
    }
    
    planet_multipliers = {
        "Sun": 1.0, "Moon": 0.8, "Mercury": 1.1, "Venus": 0.7,
        "Mars": 1.3, "Jupiter": 1.2, "Saturn": 0.9
    }
    
    degree_in_sign = planet_degree % 30
    volatility_factor = zodiac_volatility[zodiac_index] * planet_multipliers[planet_name]
    
    if degree_in_sign < 5 or degree_in_sign > 25:
        volatility_factor *= 1.2
    
    base_range_percent = 0.01 * swing_range_multiplier
    range_percent = base_range_percent * volatility_factor
    
    range_size = cmp * range_percent
    swing_low = cmp - range_size
    swing_high = cmp + range_size
    
    degree_range = 3 * volatility_factor
    degree_low = (planet_degree - degree_range) % 360
    degree_high = (planet_degree + degree_range) % 360
    
    return swing_low, swing_high, degree_low, degree_high

# Calculate timing window
def calculate_timing(dt, planet):
    base_duration = {
        "Sun": 30, "Moon": 90, "Mercury": 45, "Venus": 60,
        "Mars": 75, "Jupiter": 120, "Saturn": 150
    }
    
    duration = base_duration.get(planet, 60)
    
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
    if market == "Indian Market" and date_input.weekday() >= 5:
        st.markdown('''
        <div class="error-message">
            <strong>🚫 Market Closed</strong><br>
            The selected date is a weekend. Indian Market is closed on Saturdays and Sundays. Please select a weekday.
        </div>
        ''', unsafe_allow_html=True)
        st.stop()
    
    # Check if the selected time is outside market hours (for Indian Market)
    if market == "Indian Market" and not is_within_market_hours(time_input):
        st.markdown(f'''
        <div class="warning-message">
            <strong>⚠️ Outside Market Hours</strong><br>
            The selected time is outside Indian Market hours ({market_start.strftime("%I:%M %p")} to {market_end.strftime("%I:%M %p")}). 
            The report will show transits during market hours only.
        </div>
        ''', unsafe_allow_html=True)
    
    # Display market status
    st.markdown(f'''
    <div class="market-status">
        <h3>📊 Market Status</h3>
        <p><strong>{market} Hours:</strong> {market_start.strftime("%I:%M %p")} – {market_end.strftime("%I:%M %p")}</p>
        <p><strong>Selected Date & Time:</strong> {dt.strftime("%d %B %Y, %I:%M %p")}</p>
        <p><strong>Location:</strong> {location_input}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Get planetary positions
    planetary_positions = get_planetary_positions(dt)
    
    # Get important planet for the day
    important_planet = get_important_planet(date_input)
    
    # Display the important planet information
    st.markdown(f'''
    <div class="important-planet">
        <h2>⭐ Important Planet for Trading: {important_planet}</h2>
        <p>The ruling planet for {date_input.strftime("%A")} is {important_planet}. Pay special attention to its transit and levels during the trading session.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Calculate Moon-Rahu and Moon-Ketu transits
    moon_degree = planetary_positions.get("Moon", 0)
    moon_rahu_aspects, moon_ketu_aspects = calculate_moon_nodes_transit(dt, moon_degree)
    
    # Display Moon-Nodes Transit
    st.markdown('<div class="sub-header">🌙 Moon-Nodes Transit</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="transit-box"><h4>🔴 Moon-Rahu Transit</h4>', unsafe_allow_html=True)
        if moon_rahu_aspects:
            for aspect in moon_rahu_aspects:
                st.markdown(f'<p>{aspect["aspect"]}: {aspect["time"]}</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p>No Moon-Rahu aspects today</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="transit-box"><h4>🟡 Moon-Ketu Transit</h4>', unsafe_allow_html=True)
        if moon_ketu_aspects:
            for aspect in moon_ketu_aspects:
                st.markdown(f'<p>{aspect["aspect"]}: {aspect["time"]}</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p>No Moon-Ketu aspects today</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Prepare data for each planet
    results = []
    for planet, degree in planetary_positions.items():
        swing_low, swing_high, degree_low, degree_high = calculate_gann_levels(cmp, degree, planet)
        start_time, end_time = calculate_timing(dt, planet)
        adj_start_time, adj_end_time = adjust_timing_to_market(start_time, end_time)
        
        if market == "Indian Market" and (adj_start_time is None or adj_end_time is None):
            continue
            
        timing_str = f"{adj_start_time.strftime('%I:%M %p')} – {adj_end_time.strftime('%I:%M %p')}"
        
        if planet == "Moon":
            nakshatra = get_nakshatra(degree)
            planet_display = f"Moon in {nakshatra}"
        else:
            planet_display = planet
        
        is_important = (planet == important_planet)
        
        current_time = datetime.now().time()
        current_dt = datetime.combine(date_input, current_time)
        is_current_transit = adj_start_time <= current_dt <= adj_end_time
        
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
            st.markdown('''
            <div class="error-message">
                <strong>🚫 No Planetary Transits During Market Hours</strong><br>
                There are no planetary transits within market hours for the selected date. This could be due to:
                <ul>
                    <li>The selected date is a market holiday</li>
                    <li>All planetary transits fall outside market hours</li>
                </ul>
                Please try a different date.
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="error-message">
                <strong>🚫 No Planetary Transits Found</strong><br>
                No planetary transits were found for the selected date and time. Please try a different date or time.
            </div>
            ''', unsafe_allow_html=True)
        st.stop()
    
    # Display Symbol and CMP above the table
    st.markdown(f'<div class="symbol-cmp">📈 {symbol} | CMP: ₹{cmp:.2f}</div>', unsafe_allow_html=True)
    
    # Display the table
    st.markdown('<div class="sub-header">📊 Intraday Swing Range Analysis</div>', unsafe_allow_html=True)
    
    # Apply custom font size
    st.markdown(f"""
    <style>
        .dataframe {{
            font-size: {font_size}px !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Display the dataframe with conditional formatting
    def highlight_rows(row):
        styles = [''] * len(row)
        
        important = row['Important'] == 'Yes'
        current_transit = row['Current Transit'] == 'Yes'
        transit_nature = row['Transit Nature']
        
        if important and current_transit:
            styles = ['background-color: #ff9800; font-weight: bold; border: 2px solid #f44336;'] * len(row)
        elif current_transit:
            styles = ['background-color: #ffeb3b; border: 2px solid #ff9800;'] * len(row)
        elif important:
            styles = ['background-color: #4caf50; font-weight: bold;'] * len(row)
        elif transit_nature == 'Favorable':
            styles = ['background-color: #c8e6c9; border-left: 4px solid #4caf50;'] * len(row)
        elif transit_nature == 'Negative':
            styles = ['background-color: #ffcdd2; border-left: 4px solid #f44336;'] * len(row)
        
        return styles
    
    styled_df = df.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    # Success message
    st.markdown('''
    <div class="success-message">
        <strong>✅ Report Generated Successfully!</strong><br>
        Your Astro-Gann analysis is ready. Review the planetary transits and swing levels above.
    </div>
    ''', unsafe_allow_html=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        # PDF generation (simplified for demo)
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name=f"astro_gann_report_{date_input.strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Excel generation
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_buffer,
            file_name=f"astro_gann_report_{date_input.strftime('%Y-%m-%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# Footer
st.markdown('''
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255, 255, 255, 0.8);">
    <p>&copy; 2024 Astro-Gann Trading Tool. Combining ancient wisdom with modern market analysis.</p>
    <p>🌟 May the stars guide your trades 🌟</p>
</div>
''', unsafe_allow_html=True)
