import streamlit as st
from datetime import datetime
import pytz
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

# Sample function to simulate astro data (replace with real astrology logic/API)
def get_astro_data(date_str, location):
    return [
        ["Planet", "Sign", "Nakshatra", "Degree", "Sub Lord", "Impact"],
        ["Moon", "Cancer", "Pushya", "13°22'", "Mercury", "Bullish"],
        ["Sun", "Leo", "Magha", "5°13'", "Venus", "Bearish"],
        ["Mars", "Gemini", "Ardra", "28°47'", "Rahu", "Volatile"]
    ]

# Convert data to PDF
def create_pdf(data, filename="astro_output.pdf"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = [Paragraph("Astro Analysis Output", styles['Title']), Spacer(1, 12)]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Convert table to PNG (PNJ as requested)
def create_image(data):
    fig, ax = plt.subplots(figsize=(10, len(data)*0.5))
    ax.axis('off')
    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    return img_buffer

# Streamlit app
st.set_page_config(layout="centered")
st.title("🪐 Astro Input & Analysis")

# Input fields
date_input = st.text_input("Enter Date & Time (e.g. 7-8-2025 9:15 AM):", "7-8-2025 9:15 AM")
location_input = st.text_input("Enter Location:", "Mumbai, India")

if st.button("Generate Astro Report"):
    try:
        # Parse datetime input
        dt = datetime.strptime(date_input, "%d-%m-%Y %I:%M %p")
        astro_data = get_astro_data(dt.strftime("%Y-%m-%d %H:%M"), location_input)
        
        # Display table
        st.subheader("🧿 Astro Timeline Table")
        st.table(astro_data)

        # Generate PDF
        pdf_file = create_pdf(astro_data)
        st.download_button("📥 Download PDF", data=pdf_file, file_name="astro_report.pdf", mime="application/pdf")

        # Generate PNG
        image_file = create_image(astro_data)
        st.download_button("📥 Download PNJ", data=image_file, file_name="astro_report.pnj", mime="image/png")

    except Exception as e:
        st.error(f"Error: {e}")
