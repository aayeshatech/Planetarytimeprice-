import streamlit as st
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import pytz

# Streamlit form input
st.title("Astro Price-Timing Report Generator")

with st.form("astro_form"):
    date_input = st.date_input("Select date:")
    time_input = st.time_input("Select time:")
    location = st.text_input("Enter location (e.g., Mumbai, India):", "Mumbai, India")
    submit = st.form_submit_button("Generate Astro Report")

if submit:
    full_datetime = datetime.combine(date_input, time_input)
    local_tz = pytz.timezone("Asia/Kolkata")
    local_dt = local_tz.localize(full_datetime)

    # For flatlib
    dt = Datetime(local_dt.strftime('%Y-%m-%d'), local_dt.strftime('%H:%M'), '+05:30')
    pos = GeoPos('19.0760', '72.8777')  # Mumbai default

    chart = Chart(dt, pos)

    st.subheader("Planetary Positions:")
    for obj in ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN']:
        planet = chart.get(obj)
        st.text(f"{obj}: {planet.sign} {planet.signlon}")

    # PDF Export
    def export_pdf():
        pdf_path = "/mnt/data/astro_report.pdf"
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        story = [Paragraph("Astro Price Timing Report", styles['Title'])]

        for obj in ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN']:
            planet = chart.get(obj)
            story.append(Paragraph(f"{obj}: {planet.sign} {planet.signlon}", styles['Normal']))

        doc.build(story)
        return pdf_path

    if st.button("Download PDF"):
        pdf_file = export_pdf()
        with open(pdf_file, "rb") as f:
            st.download_button("Download Astro PDF", f, file_name="astro_report.pdf")
