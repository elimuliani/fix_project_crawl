import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="PESTEL Analysis Dashboard",
    layout="wide",
)

# Title
st.title("📊 PESTEL Analysis Dashboard")

# Load CSV file
file_path = "pln_clean.csv"  # Ganti sesuai dengan nama file CSV Anda
try:
    data = pd.read_csv(file_path)
    st.success("Data berhasil dimuat!")
except FileNotFoundError:
    st.error("File CSV tidak ditemukan. Pastikan file berada di path yang benar.")
    st.stop()

# Ensure the required columns exist
required_columns = {"headline", "content_text", "category"}
if not required_columns.issubset(data.columns):
    st.error(f"File CSV harus memiliki kolom: {required_columns}")
    st.stop()

# Group data by PESTEL categories
categories = {
    "Political": "#FFD700",  # Yellow
    "Economic": "#32CD32",  # Green
    "Social": "#1E90FF",  # Blue
    "Technological": "#8A2BE2",  # Purple
    "Environmental": "#FF6347",  # Red
    "Legal": "#FF4500",  # Orange
}

# Create a clean layout using columns
st.markdown("""
    <style>
    .category-box {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .headline {
        font-size: 16px;
        font-weight: bold;
        color: #333;
    }
    .content {
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Display each category and related news
for category, color in categories.items():
    st.markdown(f"<div class='category-box' style='background-color: {color};'>"
                f"<h3 style='color: white; text-align: center;'>{category}</h3></div>", unsafe_allow_html=True)

    # Filter news for the current category
    category_data = data[data["category"] == category]

    if category_data.empty:
        st.write("Tidak ada berita untuk kategori ini.")
    else:
        # Display the news with headline and summary
        for _, row in category_data.iterrows():
            headline = row["headline"]
            content = row["content_text"]
            st.markdown(f"<div class='headline'>{headline}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='content'>{content[:150]}...</div>", unsafe_allow_html=True)
            st.markdown("---")  # Add separator between news articles
