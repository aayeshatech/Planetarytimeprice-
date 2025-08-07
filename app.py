from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from pytz import timezone
import swisseph as swe

# === INPUTS ===
date_str = "6-8-2025"
time_str = "09:15"
location_name = "Mumbai"
latitude = 19.0760
longitude = 72.8777
timezone_str = "Asia/Kolkata"

# Nifty data
nifty_data = {
    "Open": 24574,
    "High": 24634,
    "Low": 24344,
    "Close": 24596
}

# === PARSE DATETIME ===
dt_local = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
tz = timezone(timezone_str)
dt_utc = tz.localize(dt_local).astimezone(timezone("UTC"))

# === PLANET LIST ===
planets = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu (Mean)": swe.MEAN_NODE,
    "Ketu (Mean)": swe.MEAN_NODE  # Ketu = Rahu + 180°
}

# === ASTRO DATA CALCULATION ===
jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60.0)
planet_table = []
for name, pl_code in planets.items():
    lon, _ = swe.calc_ut(jd, pl_code)
    if name == "Ketu (Mean)":
        lon = (lon[0] + 180.0) % 360.0
    planet_table.append([name, f"{lon[0]:.2f}°"])

# === PDF GENERATION ===
file_path = "/mnt/data/Nifty_Astro_Report_6Aug2025.pdf"
doc = SimpleDocTemplate(file_path, pagesize=A4)
styles = getSampleStyleSheet()
flowables = []

# Title
flowables.append(Paragraph("Nifty Astro Report", styles["Title"]))
flowables.append(Spacer(1, 12))
flowables.append(Paragraph(f"Date & Time: {dt_local.strftime('%d-%b-%Y %I:%M %p')} ({location_name})", styles["Normal"]))
flowables.append(Spacer(1, 12))

# Nifty Table
nifty_table = [
    ["Index", "Open", "High", "Low", "Close"],
    ["Nifty", nifty_data["Open"], nifty_data["High"], nifty_data["Low"], nifty_data["Close"]]
]
nifty_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER')
])
flowables.append(Paragraph("Nifty 50 Index Data:", styles["Heading3"]))
flowables.append(Table(nifty_table, style=nifty_style))
flowables.append(Spacer(1, 12))

# Planet Table
astro_table = [["Planet", "Longitude (°)"]] + planet_table
planet_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER')
])
flowables.append(Paragraph("Planetary Positions:", styles["Heading3"]))
flowables.append(Table(astro_table, style=planet_style))

# Build PDF
doc.build(flowables)

# Output file path
file_path
