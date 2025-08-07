import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Title
st.title("Astro Data Report")

# Input fields
date_input = st.date_input("Select Date", datetime.today())
time_input = st.time_input("Select Time", datetime.now().time())
location_input = st.text_input("Enter Location (e.g., Mumbai, India)", "Mumbai, India")

# Sample data structure
sample_data = {
    "Time": ["9:15 AM", "10:30 AM", "11:45 AM", "12:30 PM", "2:00 PM"],
    "Planet": ["Moon", "Mercury", "Venus", "Mars", "Jupiter"],
    "Transit Type": ["Nakshatra Change", "Sign Change", "Aspect", "Degree Change", "Sub Lord Change"],
    "Bullish/Bearish": ["Bullish", "Bearish", "Bullish", "Bearish", "Bullish"],
    "Impact": ["Nifty", "Bank Nifty", "Gold", "BTC", "Dow Jones"]
}

df = pd.DataFrame(sample_data)

# Ensure column types are consistent (fix ArrowTypeError)
for col in df.columns:
    df[col] = df[col].astype(str)

# Show table
st.subheader("Astrological Event Timeline")
st.dataframe(df)

# --- PDF Generation ---
def generate_pdf(dataframe):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Astro Data Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # Location and time
    dt_str = datetime.combine(date_input, time_input).strftime('%d %B %Y, %I:%M %p')
    elements.append(Paragraph(f"Date & Time: {dt_str}", styles['Normal']))
    elements.append(Paragraph(f"Location: {location_input}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table content
    table_data = [list(dataframe.columns)] + dataframe.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

# Download as PDF
pdf_buffer = generate_pdf(df)
st.download_button(
    label="Download PDF",
    data=pdf_buffer,
    file_name=f"astro_report_{date_input.strftime('%Y-%m-%d')}.pdf",
    mime="application/pdf"
)

# Download as Excel
excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False, engine='openpyxl')
excel_buffer.seek(0)
st.download_button(
    label="Download Excel",
    data=excel_buffer,
    file_name=f"astro_report_{date_input.strftime('%Y-%m-%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
