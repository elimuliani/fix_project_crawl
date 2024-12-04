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

# Create columns for layout
cols = st.columns(len(categories))

# Display each category and related news
for i, (category, color) in enumerate(categories.items()):
    with cols[i]:
        # Category Header with background color
        st.markdown(f"""
            <div style="background-color: {color}; padding: 20px; border-radius: 8px; margin-bottom: 10px;">
                <h3 style="text-align: center; color: white; font-size: 18px; font-weight: bold;">{category}</h3>
            </div>
        """, unsafe_allow_html=True)

        # Filter news for the current category
        category_data = data[data["category"] == category]

        if category_data.empty:
            st.write("Tidak ada berita untuk kategori ini.")
        else:
            # Display each news item under the category
            for _, row in category_data.iterrows():
                headline = row["headline"]
                content = row["content_text"]
                st.markdown(f"**{headline}**")  # Headline as bold
                st.write(f"{content[:150]}...")  # Show brief content
                st.markdown("---")  # Add separator between articles

