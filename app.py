import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import base64

# === Layout ===
st.set_page_config(page_title="Astro Report Generator", layout="centered")

st.title("🪐 Astrology Report Generator")

# Input: Date, Time
date_input = st.date_input("Select Date", datetime.now().date())
time_input = st.time_input("Select Time", datetime.now().time())

# Input: Location
location_input = st.text_input("Enter Location (City, Country)", value="Mumbai, India")

# Combine datetime
input_datetime = datetime.combine(date_input, time_input)

# Generate Button
generate = st.button("🔮 Generate Report")

# Placeholder for results
if generate:
    st.subheader("🗓️ Astro Report for:")
    st.write(f"**Date & Time:** {input_datetime.strftime('%d %B %Y, %I:%M %p')}")
    st.write(f"**Location:** {location_input}")

    # === Astro Dummy Data (replace with real astro logic or API call) ===
    st.markdown("#### 🌟 Planetary Impact Summary")
    data = {
        "Planet": ["Sun", "Moon", "Mercury", "Venus", "Mars"],
        "Sign": ["Leo", "Cancer", "Leo", "Virgo", "Taurus"],
        "Nakshatra": ["Magha", "Pushya", "Ashlesha", "Uttara Phalguni", "Rohini"],
        "Effect": ["Strong", "Neutral", "Favorable", "Strong", "Aggressive"]
    }

    for i in range(len(data["Planet"])):
        st.write(f"**{data['Planet'][i]}** in {data['Sign'][i]} ({data['Nakshatra'][i]}) → *{data['Effect'][i]}*")

    # === Chart (sample plot) ===
    st.markdown("#### 📊 Planetary Strength Chart")

    fig, ax = plt.subplots()
    strengths = [90, 60, 75, 80, 40]
    ax.bar(data["Planet"], strengths)
    ax.set_ylabel("Strength (%)")
    ax.set_ylim([0, 100])
    ax.set_title("Planetary Strengths")

    st.pyplot(fig)

    # === Download PDF ===
    def generate_pdf():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Astrological Report", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Date & Time: {input_datetime.strftime('%d %B %Y, %I:%M %p')}", styles['Normal']))
        story.append(Paragraph(f"Location: {location_input}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Planetary Effects:", styles['Heading2']))

        for i in range(len(data["Planet"])):
            story.append(Paragraph(
                f"{data['Planet'][i]} in {data['Sign'][i]} ({data['Nakshatra'][i]}) → {data['Effect'][i]}",
                styles['Normal']
            ))

        doc.build(story)
        buffer.seek(0)
        return buffer

    pdf = generate_pdf()
    st.download_button("📄 Download PDF Report", data=pdf, file_name="astro_report.pdf", mime="application/pdf")

    # === Download PNG (chart) ===
    def get_image_download_link(fig, filename="astro_chart.png"):
        img_bytes = BytesIO()
        fig.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        b64 = base64.b64encode(img_bytes.read()).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="{filename}">🖼️ Download PNG Chart</a>'
        return href

    st.markdown(get_image_download_link(fig), unsafe_allow_html=True)
