import swisseph as swe
import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

# Input
date_str = "7-8-2025"
time_str = "9:15"
location_str = "Mumbai, India"

# Convert date and time to datetime object
dt = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")

# Geolocation
geolocator = Nominatim(user_agent="astro_app")
location = geolocator.geocode(location_str)
latitude = location.latitude
longitude = location.longitude

# Timezone
tf = TimezoneFinder()
timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
timezone = pytz.timezone(timezone_str)
dt_local = timezone.localize(dt)
jd_ut = swe.julday(dt_local.year, dt_local.month, dt_local.day, dt_local.hour + dt_local.minute / 60.0)
swe.set_topo(longitude, latitude)  # Set observer location

# Get planetary positions
planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
planet_codes = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.MEAN_NODE, swe.TRUE_NODE]
positions = {}

for i, p in enumerate(planets):
    if p == "Ketu":
        lon = (360 + swe.calc_ut(jd_ut, swe.MEAN_NODE)[0][0] - 180) % 360
    else:
        lon = swe.calc_ut(jd_ut, planet_codes[i])[0][0]
    positions[p] = lon

# Display output
print(f"\nAstrological Data for {location_str} at {dt_local.strftime('%Y-%m-%d %H:%M')} ({timezone_str})")
for planet, pos in positions.items():
    print(f"{planet}: {round(pos, 2)}°")

# Save as PDF
pdf_file = "/mnt/data/astro_chart.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
styles = getSampleStyleSheet()
story = [Paragraph(f"Astrological Chart for {location_str} on {dt_local.strftime('%d-%b-%Y %H:%M %Z')}", styles['Title']), Spacer(1, 12)]

for planet, pos in positions.items():
    story.append(Paragraph(f"{planet}: {round(pos, 2)}°", styles['Normal']))

doc.build(story)

# Save as PNG (Pie Chart)
png_file = "/mnt/data/astro_chart.png"
labels = list(positions.keys())
sizes = list(positions.values())
plt.figure(figsize=(8, 8))
plt.pie([1] * len(sizes), labels=[f"{k} ({round(v, 1)}°)" for k, v in positions.items()])
plt.title("Planetary Positions")
plt.savefig(png_file)
plt.close()

print(f"\n✅ PDF and PNG generated.")
