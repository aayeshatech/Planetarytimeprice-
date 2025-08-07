import streamlit as st
from datetime import datetime
import swisseph as swe
import pytz

# Set ephemeris path
swe.set_ephe_path('/usr/share/ephe')  # Adjust if running locally

# --- INPUT SECTION ---
st.title("📈 Astro Time + Price Market View")

date_input = st.date_input("📅 Select Date", value=datetime(2025, 8, 6))
time_input = st.time_input("⏰ Select Time", value=datetime.strptime("09:15", "%H:%M").time())
location_input = st.text_input("📍 Location (for info only)", value="Mumbai, India")

nifty_high = st.number_input("Nifty High", value=24634.0)
nifty_low = st.number_input("Nifty Low", value=24344.0)
nifty_close = st.number_input("Nifty Close", value=24596.0)

# --- CONVERT TO JULIAN DAY ---
dt = datetime.combine(date_input, time_input)
timezone = pytz.timezone("Asia/Kolkata")
dt = timezone.localize(dt)
jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

# --- PLANETARY POSITIONS ---
planets = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu (Mean)': swe.MEAN_NODE,
    'Ketu (Mean)': swe.TRUE_NODE
}

planet_table = []
gann_prices = []

st.subheader("🪐 Planetary Longitudes & Price Mapping")

for name, p_id in planets.items():
    lon_tuple = swe.calc_ut(jd, p_id)[0]
    lon = lon_tuple[0]  # Extract longitude in degrees
    sign = int(lon // 30) + 1
    degree = lon % 30

    price_level = (degree / 360) * (nifty_high - nifty_low) + nifty_low
    planet_table.append([name, f"{lon:.2f}°", f"Sign {sign}", f"{price_level:.2f}"])
    gann_prices.append(price_level)

st.table(
    pd.DataFrame(planet_table, columns=["Planet", "Longitude", "Sign", "Mapped Nifty Price"])
)

# --- GANN TABLE ---
st.subheader("📐 Gann Price Levels (from astro mapping)")

gann_prices_sorted = sorted(gann_prices)
for level in gann_prices_sorted:
    st.markdown(f"🔹 **{level:.2f}**")

# --- CLOSE LEVEL COMPARISON ---
st.subheader("📊 Nifty Price Comparison")

if nifty_close in gann_prices_sorted:
    st.success("Nifty Close is exactly matching a planetary mapped level!")
else:
    # Find nearest Gann level
    nearest = min(gann_prices_sorted, key=lambda x: abs(x - nifty_close))
    st.info(f"Nifty Close: **{nifty_close:.2f}**, Nearest Astro Level: **{nearest:.2f}**")

# --- DOWNLOAD OPTION ---
st.download_button("📥 Download Astro Market Table (CSV)", 
                   data=pd.DataFrame(planet_table, columns=["Planet", "Longitude", "Sign", "Mapped Nifty Price"]).to_csv(index=False),
                   file_name="astro_market_view.csv",
                   mime='text/csv')
