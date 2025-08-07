import swisseph as swe
import pytz
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# Input
input_date_str = "2025-08-06 09:15"
location = "Mumbai, India"
nifty_data = {
    "Open": 24574,
    "High": 24634,
    "Low": 24344,
    "Close": 24596
}

# Step 1: Convert location to lat/lon and timezone
geolocator = Nominatim(user_agent="astro_app")
location_obj = geolocator.geocode(location)
latitude = location_obj.latitude
longitude = location_obj.longitude

tf = TimezoneFinder()
timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
timezone = pytz.timezone(timezone_str)

# Step 2: Convert time to UTC
local_dt = timezone.localize(datetime.strptime(input_date_str, "%Y-%m-%d %H:%M"))
utc_dt = local_dt.astimezone(pytz.utc)
jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                utc_dt.hour + utc_dt.minute / 60.0)

# Step 3: Calculate planetary positions
planets = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
    "Rahu (Mean)": swe.MEAN_NODE, "Ketu (Mean)": swe.MEAN_NODE  # Ketu = opposite
}

planet_positions = []
for planet, planet_id in planets.items():
    lon, _ = swe.calc_ut(jd, planet_id)
    if planet == "Ketu (Mean)":
        lon = (lon + 180) % 360
    sign = int(lon / 30) + 1
    deg_in_sign = lon % 30
    planet_positions.append([planet, round(lon, 2), sign, round(deg_in_sign, 2)])

# Step 4: Format as DataFrame
df = pd.DataFrame(planet_positions, columns=["Planet", "Longitude", "Sign (1-12)", "Degree in Sign"])

# Step 5: Add Nifty data row
df_nifty = pd.DataFrame([
    ["Nifty", "", "", ""],
    ["Open", nifty_data["Open"], "", ""],
    ["High", nifty_data["High"], "", ""],
    ["Low", nifty_data["Low"], "", ""],
    ["Close", nifty_data["Close"], "", ""]
], columns=["Planet", "Longitude", "Sign (1-12)", "Degree in Sign"])

df_full = pd.concat([df, df_nifty], ignore_index=True)

# Show as table
import caas_jupyter_tools as cjtools
cjtools.display_dataframe_to_user(name="Astro Table + Nifty", dataframe=df_full)

# Step 6: Export to PDF
def generate_pdf(df, filename="astro_nifty_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    style_sheet = getSampleStyleSheet()
    elements.append(Paragraph("Planetary Positions and Nifty Data", style_sheet['Heading2']))

    data = [df.columns.to_list()] + df.values.tolist()

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN',(1,1),(-1,-1),'CENTER'),
    ]))
    elements.append(table)
    doc.build(elements)

    return filename

# Generate PDF file
pdf_path = f"/mnt/data/astro_nifty_report_{utc_dt.strftime('%Y%m%d_%H%M')}.pdf"
generate_pdf(df_full, filename=pdf_path)

# Show download link
pdf_path
