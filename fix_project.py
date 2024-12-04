import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="PESTEL Analysis Dashboard",
    layout="wide",
)

# Title
st.title("PESTEL Analysis Dashboard")

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

cols = st.columns(len(categories))

# Display each category and related news
for i, (category, color) in enumerate(categories.items()):
    with cols[i]:
        st.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 10px;'>"
                    f"<h3 style='text-align: center; color: white;'>{category}</h3>"
                    f"</div>", unsafe_allow_html=True)

        # Filter news for the current category
        category_data = data[data["category"] == category]

        if category_data.empty:
            st.write("Tidak ada berita untuk kategori ini.")
        else:
            for _, row in category_data.iterrows():
                headline = row["headline"]
                content = row["content_text"]
                st.markdown(f"**{headline}**")
                st.write(content[:150] + "...")  # Tampilkan ringkasan berita

