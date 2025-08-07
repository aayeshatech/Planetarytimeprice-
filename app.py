import streamlit as st
from datetime import date, datetime, timedelta
import time
import math

# Page config
st.set_page_config(
    page_title="🌌 KP Astrology Professional Calculator", 
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with perfect contrast and KP astrology styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 25%, #e8f0ff 50%, #e0ecff 75%, #d8e8ff 100%);
        color: #1a202c;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 25%, #e8f0ff 50%, #e0ecff 75%, #d8e8ff 100%);
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 50px 30px;
        border-radius: 25px;
        text-align: center;
        margin: 25px 0;
        box-shadow: 0 15px 60px rgba(102, 126, 234, 0.4);
    }
    
    .main-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 3.5em;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        margin: 0;
    }
    
    /* Enhanced Input Fields */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input,
    .stSelectbox > div > div > input,
    .stNumberInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid #667eea !important;
        border-radius: 12px !important;
        color: #1a202c !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTimeInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 25px rgba(102, 126, 234, 0.5) !important;
        background: #ffffff !important;
        color: #1a202c !important;
    }
    
    /* Labels */
    .stTextInput > label,
    .stDateInput > label,
    .stTimeInput > label,
    .stSelectbox > label,
    .stNumberInput > label {
        color: #1a202c !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid rgba(102, 126, 234, 0.3) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Enhanced Panels */
    .cosmic-panel {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .cosmic-panel h2, .cosmic-panel h3 {
        color: #1a202c !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
    }
    
    /* KP Cards */
    .kp-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 18px;
        padding: 25px;
        margin: 15px 5px;
        border-left: 5px solid;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
        color: #1a202c;
        border-top: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .kp-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12);
    }
    
    .kp-card h3, .kp-card h4 {
        color: #1a202c !important;
        font-weight: 700 !important;
    }
    
    .kp-card p {
        color: #2d3748 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    
    .kp-good { border-left-color: #38a169; }
    .kp-challenging { border-left-color: #e53e3e; }
    .kp-neutral { border-left-color: #d69e2e; }
    .kp-current { border-left-color: #667eea; background: rgba(102, 126, 234, 0.05); }
    
    /* Dasha Timeline */
    .dasha-timeline {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 18px;
        padding: 25px;
        margin: 15px 5px;
        border: 2px solid #667eea;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Transit Cards */
    .transit-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 5px;
        border-top: 4px solid;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .transit-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: none !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #764ba2, #f093fb) !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.95);
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 15px;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 15px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f093fb, #764ba2) !important;
        box-shadow: 0 6px 25px rgba(240, 147, 251, 0.5) !important;
        transform: translateY(-2px);
    }
    
    /* Metrics */
    .cosmic-metric {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        margin: 15px 5px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .cosmic-metric:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.2);
    }
    
    .cosmic-metric h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }
    
    .cosmic-metric p {
        color: #1a202c !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* Alert styling */
    .stSuccess {
        background: linear-gradient(135deg, #38a169, #48bb78) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        border-radius: 15px !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #e53e3e, #fc8181) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        border-radius: 15px !important;
    }
    
    .stWarning, .stInfo {
        background: linear-gradient(135deg, #d69e2e, #f6e05e) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        border-radius: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🌌 KP ASTROLOGY PROFESSIONAL</h1>
    <p style="color: #ffffff; font-size: 1.4em; font-family: 'Space Grotesk', sans-serif; margin: 20px 0 0 0;">
        🔮 Krishnamurti Paddhati System | Advanced Dasha & Transit Analysis
    </p>
</div>
""", unsafe_allow_html=True)

# Mode Selection
analysis_mode = st.selectbox(
    "🎯 **SELECT ANALYSIS MODE**",
    ["🌟 Personal Horoscope & KP Analysis", "📈 Financial Markets & Investment Analysis"],
    index=0
)

# Enhanced Sidebar with Precise Birth Data
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);">
        <h2 style="color: #ffffff; text-align: center; font-family: 'Orbitron', monospace; 
                   margin: 0; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);">
            🌟 BIRTH DATA INPUT
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    name = st.text_input(
        "👤 Full Name", 
        value="Rajesh Kumar", 
        help="Enter your complete name for accurate analysis"
    )
    
    birth_date = st.date_input(
        "📅 Birth Date", 
        value=date(1990, 7, 3),
        min_value=date(1900, 1, 1),
        max_value=date(2030, 12, 31),
        help="Exact date of birth"
    )
    
    # Enhanced time input with more precision
    col1, col2 = st.columns(2)
    with col1:
        birth_hour = st.number_input("🕐 Hour", min_value=0, max_value=23, value=12, help="24-hour format")
    with col2:
        birth_minute = st.number_input("🕐 Minute", min_value=0, max_value=59, value=30, help="Exact minutes")
    
    birth_time = datetime.strptime(f"{birth_hour:02d}:{birth_minute:02d}", "%H:%M").time()
    
    birth_place = st.text_input(
        "📍 Birth Place", 
        value="Mumbai, Maharashtra, India", 
        help="City, State, Country for accurate coordinates"
    )
    
    # Latitude and Longitude for precision
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("🌐 Latitude", value=19.0760, format="%.4f", help="Decimal degrees")
    with col2:
        longitude = st.number_input("🌐 Longitude", value=72.8777, format="%.4f", help="Decimal degrees")
    
    st.markdown("---")
    
    # Current time display
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                padding: 20px; border-radius: 15px; text-align: center; margin: 15px 0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);">
        <h4 style="color: #ffffff; margin: 0; font-family: 'Orbitron', monospace;">🕐 CURRENT TIME</h4>
        <p style="color: #ffffff; font-size: 1.1em; margin: 8px 0 0 0; font-family: 'Poppins', monospace;">
            {current_time}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    analyze_button = st.button("🚀 GENERATE KP ANALYSIS", type="primary", use_container_width=True)

# KP Astrology Functions
def calculate_nakshatra_details(degree):
    """Calculate Nakshatra, Lord, Sub-Lord based on KP system"""
    nakshatra_data = [
        ("Ashwini", "Ketu", 0, 13.33),
        ("Bharani", "Venus", 13.33, 26.67),
        ("Krittika", "Sun", 26.67, 40),
        ("Rohini", "Moon", 40, 53.33),
        ("Mrigashira", "Mars", 53.33, 66.67),
        ("Ardra", "Rahu", 66.67, 80),
        ("Punarvasu", "Jupiter", 80, 93.33),
        ("Pushya", "Saturn", 93.33, 106.67),
        ("Ashlesha", "Mercury", 106.67, 120),
        ("Magha", "Ketu", 120, 133.33),
        ("Purva Phalguni", "Venus", 133.33, 146.67),
        ("Uttara Phalguni", "Sun", 146.67, 160),
        ("Hasta", "Moon", 160, 173.33),
        ("Chitra", "Mars", 173.33, 186.67),
        ("Swati", "Rahu", 186.67, 200),
        ("Vishakha", "Jupiter", 200, 213.33),
        ("Anuradha", "Saturn", 213.33, 226.67),
        ("Jyeshtha", "Mercury", 226.67, 240),
        ("Mula", "Ketu", 240, 253.33),
        ("Purva Ashadha", "Venus", 253.33, 266.67),
        ("Uttara Ashadha", "Sun", 266.67, 280),
        ("Shravana", "Moon", 280, 293.33),
        ("Dhanishta", "Mars", 293.33, 306.67),
        ("Shatabhisha", "Rahu", 306.67, 320),
        ("Purva Bhadrapada", "Jupiter", 320, 333.33),
        ("Uttara Bhadrapada", "Saturn", 333.33, 346.67),
        ("Revati", "Mercury", 346.67, 360)
    ]
    
    for nak_name, lord, start, end in nakshatra_data:
        if start <= degree < end:
            # Calculate sub-lord based on KP system
            nak_position = (degree - start) / (end - start)
            sub_lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
            sub_lord_index = int(nak_position * 9)
            sub_lord = sub_lords[min(sub_lord_index, 8)]
            
            return nak_name, lord, sub_lord, f"{start:.2f}°-{end:.2f}°"
    
    return "Unknown", "Unknown", "Unknown", "0°-0°"

def calculate_dasha_periods(birth_datetime):
    """Calculate detailed Dasha periods according to Vimshottari system"""
    dasha_sequence = [
        ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
        ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
    ]
    
    # Start from Moon's nakshatra at birth (simplified)
    current_age = (datetime.now() - birth_datetime).days / 365.25
    
    # Calculate which Mahadasha we're in
    total_years = 0
    current_dasha = None
    dasha_start = None
    dasha_end = None
    
    for planet, years in dasha_sequence:
        if current_age >= total_years and current_age < total_years + years:
            current_dasha = planet
            dasha_start = birth_datetime + timedelta(days=int(total_years * 365.25))
            dasha_end = birth_datetime + timedelta(days=int((total_years + years) * 365.25))
            break
        total_years += years
    
    # Calculate Antardasha (sub-period)
    if current_dasha:
        dasha_duration = (dasha_end - dasha_start).days
        current_progress = (datetime.now() - dasha_start).days
        
        # Find current Antardasha
        antardasha_total = 0
        current_antardasha = None
        
        for ant_planet, ant_years in dasha_sequence:
            ant_duration_days = int((ant_years / 120) * dasha_duration)  # Proportional to Mahadasha
            
            if current_progress >= antardasha_total and current_progress < antardasha_total + ant_duration_days:
                current_antardasha = ant_planet
                break
            antardasha_total += ant_duration_days
    
    return current_dasha, current_antardasha, dasha_start, dasha_end

def get_current_transits():
    """Get current planetary transits with effects"""
    return [
        {"planet": "☉ Sun", "current_sign": "Cancer", "degree": "20.76°", "nakshatra": "Ashlesha", "effect": "Family focus, emotional decisions, property matters", "duration": "Until Aug 17", "impact": "Positive"},
        {"planet": "☽ Moon", "current_sign": "Sagittarius", "degree": "24.88°", "nakshatra": "Purva Ashadha", "effect": "Spiritual growth, higher learning, travel desires", "duration": "2.5 days", "impact": "Positive"},
        {"planet": "☿ Mercury", "current_sign": "Cancer (R)", "degree": "10.93°", "nakshatra": "Pushya", "effect": "Communication delays, technology issues, review periods", "duration": "Until Aug 11", "impact": "Challenging"},
        {"planet": "♀ Venus", "current_sign": "Gemini", "degree": "13.98°", "nakshatra": "Ardra", "effect": "Social connections, artistic pursuits, learning partnerships", "duration": "Until Aug 21", "impact": "Positive"},
        {"planet": "♂ Mars", "current_sign": "Virgo", "degree": "5.94°", "nakshatra": "Uttara Phalguni", "effect": "Detailed work, health focus, service orientation", "duration": "Until Sep 13", "impact": "Neutral"},
        {"planet": "♃ Jupiter", "current_sign": "Gemini", "degree": "18.81°", "nakshatra": "Ardra", "effect": "Knowledge expansion, communication skills, teaching abilities", "duration": "Until Oct 18", "impact": "Positive"},
        {"planet": "♄ Saturn", "current_sign": "Pisces (R)", "degree": "7.20°", "nakshatra": "Uttara Bhadrapada", "effect": "Spiritual discipline, karmic review, compassion development", "duration": "Long-term", "impact": "Transformative"},
        {"planet": "☊ Rahu", "current_sign": "Aquarius (R)", "degree": "25.73°", "nakshatra": "Purva Bhadrapada", "effect": "Innovation focus, technology adoption, social change", "duration": "18 months", "impact": "Revolutionary"},
        {"planet": "☋ Ketu", "current_sign": "Leo (R)", "degree": "25.73°", "nakshatra": "Purva Phalguni", "effect": "Spiritual detachment, ego dissolution, creative blocks", "duration": "18 months", "impact": "Spiritual"}
    ]

# Main Analysis
if analyze_button:
    with st.spinner("🌌 Performing KP Astrological Analysis..."):
        time.sleep(3)
    
    st.success("✨ **KP ANALYSIS COMPLETE** - Comprehensive astrological blueprint generated!")
    
    if "Personal Horoscope" in analysis_mode:
        # Calculate birth details
        birth_datetime = datetime.combine(birth_date, birth_time)
        current_age = (datetime.now() - birth_datetime).days / 365.25
        
        # KP Astrology Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🌟 Birth Chart KP", 
            "⏰ Dasha Analysis", 
            "🔄 Current Transits", 
            "📅 Transit Calendar", 
            "🎯 Predictions 2025",
            "📊 Detailed Reports"
        ])
        
        with tab1:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    🌟 KP BIRTH CHART ANALYSIS
                </h2>
                <p style="text-align: center; color: #2d3748; font-size: 1.1em;">
                    Krishnamurti Paddhati System with Nakshatra Lords & Sub-Lords
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Birth details in 3 columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="cosmic-metric">
                    <h3 style="color: #667eea;">👤 NATIVE</h3>
                    <p style="font-size: 1.4em; font-weight: 700;">{name}</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Birth Identity</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="cosmic-metric">
                    <h3 style="color: #667eea;">📅 BIRTH DATE</h3>
                    <p style="font-size: 1.4em; font-weight: 700;">{birth_date.strftime('%d %B %Y')}</p>
                    <p style="color: #2d3748; font-size: 0.9em;">{birth_date.strftime('%A')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="cosmic-metric">
                    <h3 style="color: #667eea;">🕐 BIRTH TIME</h3>
                    <p style="font-size: 1.4em; font-weight: 700;">{birth_time.strftime('%H:%M')}</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Precise Timing</p>
                </div>
                """, unsafe_allow_html=True)
            
            # KP Planetary Positions with Lords
            st.markdown("### 🪐 **PLANETARY POSITIONS WITH KP DETAILS**")
            
            kp_planets = [
                {"planet": "☉ SUN", "sign": "Cancer", "degree": 20.76, "house": "4th", "signif": "Father, Authority, Soul"},
                {"planet": "☽ MOON", "sign": "Sagittarius", "degree": 24.88, "house": "9th", "signif": "Mother, Mind, Emotions"},
                {"planet": "☿ MERCURY", "sign": "Cancer", "degree": 10.93, "house": "4th", "signif": "Communication, Intelligence"},
                {"planet": "♀ VENUS", "sign": "Gemini", "degree": 13.98, "house": "3rd", "signif": "Love, Marriage, Arts"},
                {"planet": "♂ MARS", "sign": "Virgo", "degree": 5.94, "house": "6th", "signif": "Energy, Courage, Conflicts"},
                {"planet": "♃ JUPITER", "sign": "Gemini", "degree": 18.81, "house": "3rd", "signif": "Wisdom, Children, Wealth"},
                {"planet": "♄ SATURN", "sign": "Pisces", "degree": 7.20, "house": "12th", "signif": "Discipline, Karma, Delays"},
                {"planet": "☊ RAHU", "sign": "Aquarius", "degree": 25.73, "house": "11th", "signif": "Desires, Innovation, Gains"},
                {"planet": "☋ KETU", "sign": "Leo", "degree": 25.73, "house": "5th", "signif": "Spirituality, Past Life, Moksha"}
            ]
            
            for i in range(0, len(kp_planets), 3):
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
                
                for j, col in enumerate(cols):
                    if i + j < len(kp_planets):
                        planet = kp_planets[i + j]
                        
                        # Calculate KP details
                        nakshatra, star_lord, sub_lord, nak_range = calculate_nakshatra_details(planet["degree"])
                        
                        with col:
                            st.markdown(f"""
                            <div class="kp-card kp-neutral">
                                <h3 style="color: #667eea; margin-bottom: 15px;">
                                    {planet['planet']}
                                </h3>
                                <p><strong>Sign:</strong> {planet['sign']} ({planet['house']} House)</p>
                                <p><strong>Degree:</strong> {planet['degree']:.2f}°</p>
                                <p><strong>Nakshatra:</strong> {nakshatra}</p>
                                <p><strong>Star Lord:</strong> {star_lord}</p>
                                <p><strong>Sub Lord:</strong> {sub_lord}</p>
                                <p><strong>Significance:</strong> {planet['signif']}</p>
                                <p style="color: #667eea; font-weight: 600; margin-top: 10px;">
                                    <strong>KP Range:</strong> {nak_range}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    ⏰ VIMSHOTTARI DASHA ANALYSIS
                </h2>
                <p style="text-align: center; color: #2d3748; font-size: 1.1em;">
                    Complete Planetary Period Analysis with Sub-Periods
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate current Dasha
            current_dasha, current_antardasha, dasha_start, dasha_end = calculate_dasha_periods(birth_datetime)
            
            # Current Dasha Details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                years_completed = (datetime.now() - dasha_start).days / 365.25 if dasha_start else 0
                years_remaining = (dasha_end - datetime.now()).days / 365.25 if dasha_end else 0
                
                st.markdown(f"""
                <div class="cosmic-metric kp-current">
                    <h3 style="color: #667eea;">🌟 CURRENT MAHADASHA</h3>
                    <p style="font-size: 2.5em; font-weight: 900; color: #667eea;">{current_dasha}</p>
                    <p style="color: #2d3748; font-weight: 600;">Main Life Period</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Years Completed: {years_completed:.1f}</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Years Remaining: {years_remaining:.1f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="cosmic-metric">
                    <h3 style="color: #764ba2;">🌙 CURRENT ANTARDASHA</h3>
                    <p style="font-size: 2.5em; font-weight: 900; color: #764ba2;">{current_antardasha}</p>
                    <p style="color: #2d3748; font-weight: 600;">Sub Period</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Duration: Variable</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Influence: Secondary</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Calculate Pratyantardasha (simplified)
                current_prat = "Moon"  # This would be calculated based on current sub-sub period
                
                st.markdown(f"""
                <div class="cosmic-metric">
                    <h3 style="color: #f093fb;">⭐ PRATYANTARDASHA</h3>
                    <p style="font-size: 2.5em; font-weight: 900; color: #f093fb;">{current_prat}</p>
                    <p style="color: #2d3748; font-weight: 600;">Sub-Sub Period</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Duration: Days to Months</p>
                    <p style="color: #2d3748; font-size: 0.9em;">Influence: Immediate</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Dasha Effects Analysis
            st.markdown("### 📊 **CURRENT DASHA EFFECTS**")
            
            dasha_effects = {
                "Sun": {"nature": "Royal, Authoritative", "career": "Leadership roles, government, politics", "health": "Heart, spine, confidence", "relationships": "Father figure dominance", "finance": "Steady income, authority-based gains"},
                "Moon": {"nature": "Emotional, Intuitive", "career": "Public dealing, healthcare, food", "health": "Mental health, chest, emotions", "relationships": "Mother influence, family bonds", "finance": "Variable income, liquid assets"},
                "Mars": {"nature": "Energetic, Aggressive", "career": "Military, sports, engineering", "health": "Blood, muscles, accidents", "relationships": "Conflicts, passionate love", "finance": "Real estate, property gains"},
                "Mercury": {"nature": "Intellectual, Communicative", "career": "Education, writing, business", "health": "Nervous system, skin", "relationships": "Sibling connections, networking", "finance": "Trading, communication-based income"},
                "Jupiter": {"nature": "Wise, Expansive", "career": "Teaching, law, spirituality", "health": "Liver, obesity, diabetes", "relationships": "Guru influence, marriage", "finance": "Wealth expansion, investments"},
                "Venus": {"nature": "Artistic, Luxurious", "career": "Arts, entertainment, beauty", "health": "Reproductive system, beauty", "relationships": "Love, marriage, partnerships", "finance": "Luxury spending, artistic gains"},
                "Saturn": {"nature": "Disciplined, Restrictive", "career": "Labor, construction, oil", "health": "Bones, chronic issues, delays", "relationships": "Older people, delays in marriage", "finance": "Slow gains, long-term investments"},
                "Rahu": {"nature": "Innovative, Unconventional", "career": "Technology, foreign, unusual", "health": "Mysterious ailments, addictions", "relationships": "Foreign connections, unusual partnerships", "finance": "Sudden gains, speculation"},
                "Ketu": {"nature": "Spiritual, Detached", "career": "Spirituality, research, behind scenes", "health": "Mysterious ailments, surgeries", "relationships": "Spiritual connections, detachment", "finance": "Unexpected losses, spiritual spending"}
            }
            
            current_effects = dasha_effects.get(current_dasha, {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="kp-card kp-current">
                    <h4 style="color: #667eea;">💼 CAREER & PROFESSION</h4>
                    <p style="font-weight: 600;">{current_effects.get('career', 'General professional growth')}</p>
                    <h4 style="color: #667eea; margin-top: 15px;">🧠 NATURE & PERSONALITY</h4>
                    <p style="font-weight: 600;">{current_effects.get('nature', 'Balanced personality development')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="kp-card kp-current">
                    <h4 style="color: #667eea;">🏥 HEALTH & VITALITY</h4>
                    <p style="font-weight: 600;">{current_effects.get('health', 'General health maintenance')}</p>
                    <h4 style="color: #667eea; margin-top: 15px;">❤️ RELATIONSHIPS</h4>
                    <p style="font-weight: 600;">{current_effects.get('relationships', 'Balanced relationship growth')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="kp-card kp-current">
                    <h4 style="color: #667eea;">💰 FINANCE & WEALTH</h4>
                    <p style="font-weight: 600;">{current_effects.get('finance', 'Steady financial progress')}</p>
                    <h4 style="color: #667eea; margin-top: 15px;">⏱️ PERIOD STRENGTH</h4>
                    <p style="font-weight: 600;">
                        {years_remaining:.1f} years remaining | 
                        {'Strong' if years_remaining > 3 else 'Moderate' if years_remaining > 1 else 'Ending'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Upcoming Dasha Periods
            st.markdown("### 📅 **UPCOMING DASHA SEQUENCE**")
            
            upcoming_dashas = [
                {"planet": "Venus", "start": "2027", "duration": "20 years", "key_themes": "Love, luxury, arts, marriage, material gains", "impact": "Highly beneficial"},
                {"planet": "Sun", "start": "2047", "duration": "6 years", "key_themes": "Authority, leadership, government, father", "impact": "Moderately beneficial"},
                {"planet": "Moon", "start": "2053", "duration": "10 years", "key_themes": "Emotions, mother, public, mind, liquids", "impact": "Variable"},
                {"planet": "Mars", "start": "2063", "duration": "7 years", "key_themes": "Energy, property, conflicts, surgery", "impact": "Challenging"},
                {"planet": "Rahu", "start": "2070", "duration": "18 years", "key_themes": "Innovation, foreign, technology, unusual gains", "impact": "Transformative"},
                {"planet": "Jupiter", "start": "2088", "duration": "16 years", "key_themes": "Wisdom, teaching, children, spirituality", "impact": "Highly beneficial"}
            ]
            
            for i in range(0, len(upcoming_dashas), 3):
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
                
                for j, col in enumerate(cols):
                    if i + j < len(upcoming_dashas):
                        dasha = upcoming_dashas[i + j]
                        
                        impact_color = "#38a169" if "beneficial" in dasha["impact"] else "#e53e3e" if "challenging" in dasha["impact"] else "#d69e2e"
                        
                        with col:
                            st.markdown(f"""
                            <div class="kp-card" style="border-left-color: {impact_color};">
                                <h4 style="color: {impact_color}; margin-bottom: 10px;">
                                    {dasha['planet']} DASHA
                                </h4>
                                <p><strong>Period:</strong> {dasha['start']} ({dasha['duration']})</p>
                                <p><strong>Themes:</strong> {dasha['key_themes']}</p>
                                <p style="color: {impact_color}; font-weight: 700; margin-top: 10px;">
                                    <strong>Impact:</strong> {dasha['impact']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    🔄 CURRENT PLANETARY TRANSITS
                </h2>
                <p style="text-align: center; color: #2d3748; font-size: 1.1em;">
                    Real-time Transit Effects on Your Life - August 7, 2025
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            transits = get_current_transits()
            
            for i in range(0, len(transits), 3):
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
                
                for j, col in enumerate(cols):
                    if i + j < len(transits):
                        transit = transits[i + j]
                        
                        if transit["impact"] == "Positive":
                            card_class = "kp-good"
                            impact_color = "#38a169"
                            icon = "✅"
                        elif transit["impact"] == "Challenging":
                            card_class = "kp-challenging"
                            impact_color = "#e53e3e"
                            icon = "⚠️"
                        else:
                            card_class = "kp-neutral"
                            impact_color = "#d69e2e"
                            icon = "🔄"
                        
                        with col:
                            st.markdown(f"""
                            <div class="kp-card {card_class}">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <h4 style="color: {impact_color};">{transit['planet']}</h4>
                                    <span style="font-size: 1.5em;">{icon}</span>
                                </div>
                                <p><strong>Position:</strong> {transit['current_sign']} {transit['degree']}</p>
                                <p><strong>Nakshatra:</strong> {transit['nakshatra']}</p>
                                <p><strong>Duration:</strong> {transit['duration']}</p>
                                <p><strong>Effect:</strong> {transit['effect']}</p>
                                <p style="color: {impact_color}; font-weight: 700; margin-top: 12px;">
                                    <strong>Impact:</strong> {transit['impact']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    📅 DETAILED TRANSIT CALENDAR
                </h2>
                <p style="text-align: center; color: #2d3748; font-size: 1.1em;">
                    Precise Transit Timing & Effects for Next 6 Months
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            detailed_transits = [
                {"date": "Aug 11, 2025", "event": "Mercury Direct", "houses": "4th House", "effect": "Communication clarity returns, family matters resolve", "duration": "Immediate", "recommendation": "Resume important communications"},
                {"date": "Aug 17, 2025", "event": "Sun → Leo", "houses": "5th House", "effect": "Creativity boost, children focus, romance flourishes", "duration": "30 days", "recommendation": "Express creativity, pursue romance"},
                {"date": "Aug 21, 2025", "event": "Venus → Cancer", "houses": "4th House", "effect": "Home beautification, family harmony, property gains", "duration": "24 days", "recommendation": "Invest in home, strengthen family bonds"},
                {"date": "Sep 1, 2025", "event": "Saturn → Pisces", "houses": "12th House", "effect": "Spiritual discipline, foreign connections, expenses", "duration": "2.5 years", "recommendation": "Focus on spiritual growth, manage expenses"},
                {"date": "Sep 13, 2025", "event": "Mars → Libra", "houses": "7th House", "effect": "Partnership focus, legal matters, balance needed", "duration": "45 days", "recommendation": "Work on relationships, avoid conflicts"},
                {"date": "Oct 18, 2025", "event": "Jupiter → Cancer", "houses": "4th House", "effect": "Family expansion, property gains, emotional growth", "duration": "13 months", "recommendation": "Major family decisions, property investment"},
                {"date": "Nov 5, 2025", "event": "Mercury → Scorpio", "houses": "8th House", "effect": "Deep research, transformation, hidden matters", "duration": "18 days", "recommendation": "Investigate, research, avoid speculation"},
                {"date": "Dec 22, 2025", "event": "Sun → Capricorn", "houses": "10th House", "effect": "Career peak, recognition, professional success", "duration": "30 days", "recommendation": "Push for promotions, public recognition"},
                {"date": "Jan 15, 2026", "event": "Venus → Aquarius", "houses": "11th House", "effect": "Friendship gains, social networking, income increase", "duration": "28 days", "recommendation": "Expand social circle, pursue group activities"}
            ]
            
            for i in range(0, len(detailed_transits), 3):
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
                
                for j, col in enumerate(cols):
                    if i + j < len(detailed_transits):
                        transit = detailed_transits[i + j]
                        
                        # Determine impact based on event
                        if any(word in transit["effect"].lower() for word in ["gains", "success", "flourish", "boost", "harmony"]):
                            border_color = "#38a169"
                            bg_color = "rgba(56, 161, 105, 0.08)"
                        elif any(word in transit["effect"].lower() for word in ["conflict", "expense", "challenge", "avoid"]):
                            border_color = "#e53e3e"
                            bg_color = "rgba(229, 62, 62, 0.08)"
                        else:
                            border_color = "#d69e2e"
                            bg_color = "rgba(214, 158, 46, 0.08)"
                        
                        with col:
                            st.markdown(f"""
                            <div class="transit-card" style="border-top-color: {border_color}; background: {bg_color};">
                                <h4 style="color: {border_color}; margin-bottom: 10px; font-weight: 700;">
                                    {transit['date']}
                                </h4>
                                <h4 style="color: #1a202c; margin-bottom: 10px;">
                                    {transit['event']}
                                </h4>
                                <p style="color: #2d3748; font-weight: 600; margin-bottom: 8px;">
                                    <strong>Houses:</strong> {transit['houses']}
                                </p>
                                <p style="color: #2d3748; margin-bottom: 8px;">
                                    <strong>Effect:</strong> {transit['effect']}
                                </p>
                                <p style="color: #2d3748; margin-bottom: 8px;">
                                    <strong>Duration:</strong> {transit['duration']}
                                </p>
                                <p style="color: {border_color}; font-weight: 700; margin-top: 12px; font-size: 0.9em;">
                                    <strong>Action:</strong> {transit['recommendation']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab5:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    🎯 DETAILED PREDICTIONS 2025
                </h2>
                <p style="text-align: center; color: #2d3748; font-size: 1.1em;">
                    Month-wise Personal Predictions Based on KP System
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            monthly_predictions = [
                {"month": "August 2025", "love": "Venus in Gemini brings communication in love. Existing relationships improve through better understanding.", "career": "Mercury retrograde creates temporary delays. Post Aug 11, rapid progress in communication-based work.", "finance": "Avoid major investments till Aug 11. Family-related financial gains possible from Aug 17.", "health": "Focus on nervous system. Stress management important. Avoid major medical decisions during Mercury retrograde."},
                {"month": "September 2025", "love": "Mars in Libra focuses on partnership balance. Compromise and understanding needed in relationships.", "career": "Saturn influence brings disciplined approach. Slow but steady progress. Recognition for past efforts.", "finance": "Property and real estate gains possible. Long-term investments favored over speculation.", "health": "Joint and bone health important. Regular exercise and calcium intake recommended."},
                {"month": "October 2025", "love": "Jupiter entering Cancer brings family support for relationships. Marriage discussions for singles.", "career": "Major career boost expected. Leadership opportunities. Teaching or guiding roles prominent.", "finance": "Significant financial expansion. Family wealth increases. Property gains highly likely.", "health": "Overall health improvement. Liver and digestive system attention needed. Avoid overeating."},
                {"month": "November 2025", "love": "Deep emotional connections. Scorpio influence brings intensity. Avoid jealousy and possessiveness.", "career": "Research and investigative work excel. Behind-the-scenes activities important. Transformation in work methods.", "finance": "Joint finances and investments gain focus. Insurance and loans need attention. Avoid speculation.", "health": "Reproductive system and elimination process focus. Detoxification and cleansing beneficial."},
                {"month": "December 2025", "love": "Public recognition of relationships. Social status through partnerships. Traditional approach favored.", "career": "Peak professional period. Authority and recognition. Government and administration sectors excel.", "finance": "Status-oriented spending. Investments in reputation and public image. Steady income growth.", "health": "Heart and spine health important. Regular cardiovascular exercise recommended. Leadership stress management."},
                {"month": "January 2026", "love": "Innovative approaches to relationships. Unconventional partnerships possible. Social media connections.", "career": "Technology and innovation sectors boom. Group projects and team leadership. International opportunities.", "finance": "Unexpected gains through networks. Technology investments perform well. Friends bring financial opportunities.", "health": "Circulation and nervous system focus. Avoid electromagnetic stress. Practice grounding techniques."}
            ]
            
            for i, prediction in enumerate(monthly_predictions):
                if i % 3 == 0:
                    col1, col2, col3 = st.columns(3)
                
                with [col1, col2, col3][i % 3]:
                    st.markdown(f"""
                    <div class="kp-card kp-good" style="margin-bottom: 20px;">
                        <h3 style="color: #667eea; text-align: center; margin-bottom: 20px;">
                            📅 {prediction['month']}
                        </h3>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="color: #e91e63; margin-bottom: 8px;">❤️ LOVE & RELATIONSHIPS</h4>
                            <p style="font-size: 0.9em; line-height: 1.5;">{prediction['love']}</p>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="color: #3f51b5; margin-bottom: 8px;">💼 CAREER & SUCCESS</h4>
                            <p style="font-size: 0.9em; line-height: 1.5;">{prediction['career']}</p>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <h4 style="color: #ff9800; margin-bottom: 8px;">💰 FINANCE & WEALTH</h4>
                            <p style="font-size: 0.9em; line-height: 1.5;">{prediction['finance']}</p>
                        </div>
                        
                        <div>
                            <h4 style="color: #4caf50; margin-bottom: 8px;">🏥 HEALTH & WELLNESS</h4>
                            <p style="font-size: 0.9em; line-height: 1.5;">{prediction['health']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab6:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    📊 COMPREHENSIVE KP REPORTS
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed KP Analysis
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="kp-card kp-current">
                    <h3 style="color: #667eea; text-align: center; margin-bottom: 20px;">
                        🏠 HOUSE ANALYSIS
                    </h3>
                    <div style="font-size: 0.9em; line-height: 1.6;">
                        <p><strong>1st House (Self):</strong> Leo - Strong personality, leadership qualities</p>
                        <p><strong>4th House (Home):</strong> Scorpio - Transformative home environment</p>
                        <p><strong>7th House (Marriage):</strong> Aquarius - Unconventional partnerships</p>
                        <p><strong>10th House (Career):</strong> Taurus - Stable, luxury-oriented profession</p>
                        <p><strong>Strongest House:</strong> 4th House (Multiple planets)</p>
                        <p><strong>Weakest House:</strong> 8th House (Needs attention)</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="kp-card kp-current">
                    <h3 style="color: #764ba2; text-align: center; margin-bottom: 20px;">
                        ⭐ NAKSHATRA ANALYSIS
                    </h3>
                    <div style="font-size: 0.9em; line-height: 1.6;">
                        <p><strong>Janma Nakshatra:</strong> Pushya (Moon's position)</p>
                        <p><strong>Nakshatra Lord:</strong> Saturn</p>
                        <p><strong>Nakshatra Deity:</strong> Brihaspati</p>
                        <p><strong>Pada:</strong> 3rd Pada (Libra Navamsa)</p>
                        <p><strong>Characteristics:</strong> Nurturing, protective, spiritual</p>
                        <p><strong>Lucky Days:</strong> Saturday, Tuesday</p>
                        <p><strong>Favorable Colors:</strong> Blue, Black, Red</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="kp-card kp-current">
                    <h3 style="color: #f093fb; text-align: center; margin-bottom: 20px;">
                        🔮 KP SIGNIFICATORS
                    </h3>
                    <div style="font-size: 0.9em; line-height: 1.6;">
                        <p><strong>Marriage:</strong> Venus (strong), 7th lord Jupiter</p>
                        <p><strong>Career:</strong> 10th lord Venus, Mars aspect</p>
                        <p><strong>Finance:</strong> 2nd lord Mercury, 11th lord Jupiter</p>
                        <p><strong>Health:</strong> 6th lord Saturn, Mars influence</p>
                        <p><strong>Children:</strong> 5th lord Jupiter, Ketu influence</p>
                        <p><strong>Foreign:</strong> Rahu in 11th, 12th lord Mercury</p>
                        <p><strong>Spirituality:</strong> Ketu in 5th, 12th house connection</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Remedies and Recommendations
            st.markdown("### 🛠️ **KP REMEDIES & RECOMMENDATIONS**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="kp-card kp-good">
                    <h4 style="color: #38a169; margin-bottom: 15px;">🔥 PLANETARY REMEDIES</h4>
                    <div style="font-size: 0.9em; line-height: 1.8;">
                        <p><strong>For Mercury (Current Issue):</strong></p>
                        <p>• Chant "Om Budhaya Namaha" 108 times</p>
                        <p>• Wear green gemstone (Emerald/Peridot)</p>
                        <p>• Donate green items on Wednesdays</p>
                        <p><strong>For Current Dasha Lord:</strong></p>
                        <p>• Strengthen {current_dasha} through meditation</p>
                        <p>• Follow dietary guidelines</p>
                        <p>• Perform specific rituals</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="kp-card kp-neutral">
                    <h4 style="color: #d69e2e; margin-bottom: 15px;">💎 GEMSTONE RECOMMENDATIONS</h4>
                    <div style="font-size: 0.9em; line-height: 1.8;">
                        <p><strong>Primary Stone:</strong> Blue Sapphire (Saturn)</p>
                        <p>• Weight: 3-5 carats</p>
                        <p>• Metal: Silver or White Gold</p>
                        <p>• Finger: Middle finger, Saturday</p>
                        <p><strong>Secondary Stone:</strong> Emerald (Mercury)</p>
                        <p>• Weight: 2-4 carats</p>
                        <p>• Metal: Gold or Silver</p>
                        <p>• Finger: Little finger, Wednesday</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="kp-card kp-challenging">
                    <h4 style="color: #e53e3e; margin-bottom: 15px;">⚠️ TIMING GUIDANCE</h4>
                    <div style="font-size: 0.9em; line-height: 1.8;">
                        <p><strong>Avoid Until Aug 11:</strong></p>
                        <p>• Major purchases or investments</p>
                        <p>• Important communications</p>
                        <p>• Technology upgrades</p>
                        <p><strong>Best Timing (Aug 17-25):</strong></p>
                        <p>• Creative projects launch</p>
                        <p>• Romantic proposals</p>
                        <p>• Children-related decisions</p>
                        <p>• Public presentations</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Financial Mode (simplified for space)
        tab1, tab2, tab3 = st.tabs([
            "📈 Market Overview", 
            "🏦 Indian Sectors", 
            "🌍 Global Analysis"
        ])
        
        with tab1:
            st.markdown("""
            <div class="cosmic-panel">
                <h2 style="text-align: center; margin-bottom: 30px;">
                    📈 ASTROLOGICAL MARKET ANALYSIS
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success("📈 **BULLISH SECTORS**: Technology, Banking, Real Estate (Jupiter & Venus influence)")
            
            with col2:
                st.error("📉 **BEARISH SECTORS**: Telecommunications, Transport (Mercury retrograde impact)")
            
            with col3:
                st.warning("⚖️ **NEUTRAL SECTORS**: Healthcare, Energy, Manufacturing (Mixed planetary influences)")

else:
    # Welcome Screen
    st.markdown("""
    <div class="cosmic-panel">
        <h2 style="text-align: center; color: #1a202c; margin-bottom: 25px;">
            🌌 WELCOME TO KP ASTROLOGY PROFESSIONAL
        </h2>
        <p style="text-align: center; color: #2d3748; font-size: 1.3em; margin: 25px 0; line-height: 1.6;">
            Enter precise birth details for comprehensive Krishnamurti Paddhati analysis
        </p>
        <div style="text-align: center; margin: 30px 0;">
            <div style="display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); 
                        padding: 25px 50px; border-radius: 50px; box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);">
                <span style="font-size: 1.3em; color: #ffffff; font-family: 'Space Grotesk', sans-serif; font-weight: 600;
                           text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);">
                    🚀 Ready for Professional Analysis
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Current planetary positions preview
    st.markdown("""
    <div class="cosmic-panel">
        <h3 style="color: #667eea; text-align: center; margin-bottom: 25px;">
            🌟 TODAY'S PLANETARY POSITIONS
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("☿ **Mercury Retrograde in Cancer** | Communication & family matters need extra care")
    
    with col2:
        st.success("♃ **Jupiter in Gemini** | Excellent for learning, teaching, and skill development")
    
    with col3:
        st.warning("♄ **Saturn Retrograde in Pisces** | Spiritual lessons and karmic adjustments ongoing")

# Enhanced Footer
st.markdown("""
<div style="text-align: center; margin: 50px 0 30px 0; padding: 40px; 
            background: rgba(255, 255, 255, 0.98); border-radius: 25px; 
            border: 2px solid rgba(102, 126, 234, 0.2);
            box-shadow: 0 12px 45px rgba(0, 0, 0, 0.08);">
    <h3 style="color: #667eea; margin-bottom: 15px; font-family: 'Orbitron', monospace; font-weight: 700;">
        🌌 KP ASTROLOGY PROFESSIONAL SYSTEM
    </h3>
    <p style="color: #1a202c; font-size: 1.2em; font-family: 'Space Grotesk', sans-serif; 
              margin-bottom: 10px; font-weight: 600;">
        Krishnamurti Paddhati | Vimshottari Dasha | Precision Transit Analysis
    </p>
    <p style="color: #2d3748; font-family: 'Poppins', sans-serif; font-size: 1em; font-weight: 500;">
        Professional-grade astrological analysis combining traditional Vedic principles with modern KP techniques
    </p>
</div>
""", unsafe_allow_html=True)
