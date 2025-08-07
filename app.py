import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime
from geopy.geocoders import Nominatim
import pytz
import pandas as pd

# ---------- Location Finder ----------
@st.cache_data(show_spinner=False)
def get_location_coords(location_name):
    geolocator = Nominatim(user_agent="astro-app")
    location = geolocator.geocode(location_name)
    if location and 'country_code' in location.raw.get('address', {}):
        country_code = location.raw['address']['country_code']
        timezone_str = pytz.country_timezones(country_code)[0]
        return location.latitude, location.longitude, timezone_str
    elif location:
        return location.latitude, location.longitude, 'UTC'
    return None, None, None

# ---------- DO NOT CACHE: Not Serializable ----------
def load_planets():
    return load('de421.bsp')

# ---------- Position Calculator ----------
def get_planet_positions(date_str, time_str, lat, lon, tz_str):
    planets = load_planets()
    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

    local_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
    tz = pytz.timezone(tz_str)
    local_dt = tz.localize(local_time)
    utc_dt = local_dt.astimezone(pytz.utc)

    ts = load.timescale()
    t = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute)

    data = []
    for name in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter barycenter', 'saturn barycenter']:
        body = planets[name]
        astrometric = observer.at(t).observe(body).apparent()
        ra, dec, distance = astrometric.radec()
        alt, az, _ = astrometric.altaz()
        data.append({
            'Planet': name.title(),
            'RA (hrs)': round(ra.hours, 4),
            'Dec (°)': round(dec.degrees, 4),
            'Altitude (°)': round(alt.degrees, 4)
        })

    return pd.DataFrame(data)
