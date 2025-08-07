import math
import datetime

# === INPUT ===
symbol_name = "Nifty"
current_price = 24574
base_degree = 0       # Can be 0 for Gann 360 system
base_price = 144      # 1 degree = ₹1.6875 (24480/144°) approx

# === FUNCTION TO CALCULATE PRICE AT GANN DEGREE ===
def price_from_degree(degree):
    return round(base_price * (degree / 1), 2)

def degree_from_price(price):
    return round((price / base_price) * 1, 2)

# === SWING RANGE CALCULATION (±4° to ±6° range) ===
intraday_swing_degrees = [0, 2, 4, 6, 8, 10, 12, 16, 24, 30, 36, 45, 60, 72, 90, 120, 144, 150, 180, 210, 240, 270, 288, 300, 315, 330, 345, 360]

# Calculate nearest base degree
price_deg = degree_from_price(current_price)
base_deg = min(intraday_swing_degrees, key=lambda x: abs(x - price_deg))

# Get ±range (one level above/below)
idx = intraday_swing_degrees.index(base_deg)
levels = []
if idx > 0:
    levels.append(intraday_swing_degrees[idx - 1])
levels.append(base_deg)
if idx < len(intraday_swing_degrees) - 1:
    levels.append(intraday_swing_degrees[idx + 1])

# Generate support-resistance levels
levels_prices = [(deg, price_from_degree(deg)) for deg in levels]

# === OUTPUT ===
print(f"\n🔹 Symbol: {symbol_name.upper()}  |  CMP: ₹{current_price}")
print("🔹 Gann Swing Levels:")
for deg, price in levels_prices:
    tag = "(CMP)" if math.isclose(price, current_price, abs_tol=5) else ""
    print(f"   → {deg:>3}° = ₹{price:>7} {tag}")

# === Optional: Astro Link ===
# Example: You can map planet to price based on degree
planet_degrees = {
    "Sun": 144,
    "Moon": 90,
    "Mercury": 72,
    "Venus": 60,
    "Mars": 36,
    "Jupiter": 120,
    "Saturn": 288
}
print("\n🔹 Planetary Price Map:")
for planet, deg in planet_degrees.items():
    price = price_from_degree(deg)
    print(f"   → {planet:<8} @ {deg:>3}° = ₹{price}")

# === Optional: Time Alert Tagging ===
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"\n🕒 Generated at {now}")
