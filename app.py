import tkinter as tk
from tkinter import filedialog
from flatlib.chart import Chart
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.const import PLANETS
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def get_transits(date_str, time_str, place_lat, place_lon):
    dt = Datetime(f'{date_str}', f'{time_str}', '+05:30')  # IST
    pos = GeoPos(place_lat, place_lon)
    chart = Chart(dt, pos)
    data = []
    for planet in PLANETS:
        obj = chart.get(planet)
        data.append([planet, obj.sign, f'{round(obj.lon, 2)}°'])
    return data

def show_result():
    date_str = date_entry.get()
    time_str = time_entry.get()
    lat = lat_entry.get()
    lon = lon_entry.get()

    table_data = [["Planet", "Sign", "Degree"]]
    result = get_transits(date_str, time_str, lat, lon)
    table_data.extend(result)

    for row in table_data:
        output.insert(tk.END, "\t".join(row) + "\n")

def export_pdf():
    table_data = [["Planet", "Sign", "Degree"]]
    result = get_transits(date_entry.get(), time_entry.get(), lat_entry.get(), lon_entry.get())
    table_data.extend(result)

    pdf = SimpleDocTemplate("astro_transits.pdf")
    table = Table(table_data)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                               ("GRID", (0, 0), (-1, -1), 1, colors.black)]))
    pdf.build([table])

app = tk.Tk()
app.title("Dynamic Astro Transit Layout")

tk.Label(app, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
date_entry = tk.Entry(app)
date_entry.insert(0, "2025-08-07")
date_entry.grid(row=0, column=1)

tk.Label(app, text="Time (HH:MM):").grid(row=1, column=0)
time_entry = tk.Entry(app)
time_entry.insert(0, "09:15")
time_entry.grid(row=1, column=1)

tk.Label(app, text="Latitude:").grid(row=2, column=0)
lat_entry = tk.Entry(app)
lat_entry.insert(0, "19.0760")  # Mumbai latitude
lat_entry.grid(row=2, column=1)

tk.Label(app, text="Longitude:").grid(row=3, column=0)
lon_entry = tk.Entry(app)
lon_entry.insert(0, "72.8777")  # Mumbai longitude
lon_entry.grid(row=3, column=1)

tk.Button(app, text="Show Transit", command=show_result).grid(row=4, column=0)
tk.Button(app, text="Export PDF", command=export_pdf).grid(row=4, column=1)

output = tk.Text(app, height=15, width=60)
output.grid(row=5, column=0, columnspan=2)

app.mainloop()
