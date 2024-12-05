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
file_path = "pln_clean.csv"  # Ganti dengan nama file CSV Anda
try:
    data = pd.read_csv(file_path)
    st.success("Data berhasil dimuat!")
except FileNotFoundError:
    st.error("File CSV tidak ditemukan. Pastikan file berada di path yang benar.")
    st.stop()

# Ensure the required columns exist
required_columns = {"headline", "link", "category"}
if not required_columns.issubset(data.columns):
    st.error(f"File CSV harus memiliki kolom: {required_columns}")
    st.stop()

# Group data by PESTEL categories
categories = {
    "Politik": "#FFD700",  # Yellow
    "Ekonomi": "#32CD32",  # Green
    "Sosial": "#1E90FF",  # Blue
    "Teknologi": "#8A2BE2",  # Purple
    "Lingkungan": "#FF6347",  # Red
    "Legal": "#FF4500",  # Orange
}

# Streamlit columns for categories
cols = st.columns(len(categories))

# Display each category and its clickable headlines with pagination
items_per_page = 5  # Number of items per page

for i, (category, color) in enumerate(categories.items()):
    with cols[i]:
        st.markdown(f"<div style='background-color: {color}; padding: 5px; border-radius: 10px;'>"
                    f"<h4 style='text-align: center; color: white;'>{category}</h4>"
                    f"</div>", unsafe_allow_html=True)

        # Filter news for the current category
        category_data = data[data["category"] == category]

        if category_data.empty:
            st.write("Tidak ada berita.")
        else:
            # Session state for current page
            if f"page_{category}" not in st.session_state:
                st.session_state[f"page_{category}"] = 1

            # Calculate pagination
            total_items = len(category_data)
            total_pages = (total_items - 1) // items_per_page + 1
            current_page = st.session_state[f"page_{category}"]

            start_idx = (current_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_data = category_data.iloc[start_idx:end_idx]

            # Display paginated headlines
            for _, row in page_data.iterrows():
                headline = row["headline"]
                link = row["link"]
                # Display clickable headline
                st.markdown(f"- [{headline}]({link})")

            # Add minimalistic pagination controls
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; margin-top: 10px;">
                    <button onclick="window.location.reload()" style="
                        font-size: 10px; 
                        padding: 2px 6px; 
                        margin-right: 10px; 
                        border: 1px solid #ccc; 
                        border-radius: 3px; 
                        background-color: #f9f9f9; 
                        cursor: pointer;"
                        {'' if current_page > 1 else 'disabled'}>-</button>
                    <span style="margin: 0 5px; font-size: 12px;">Halaman {current_page}/{total_pages}</span>
                    <button onclick="window.location.reload()" style="
                        font-size: 10px; 
                        padding: 2px 6px; 
                        margin-left: 10px; 
                        border: 1px solid #ccc; 
                        border-radius: 3px; 
                        background-color: #f9f9f9; 
                        cursor: pointer;"
                        {'' if current_page < total_pages else 'disabled'}>+</button>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Update session state for buttons
            if st.button("", key=f"prev_{category}"):
                if current_page > 1:
                    st.session_state[f"page_{category}"] -= 1
            if st.button("", key=f"next_{category}"):
                if current_page < total_pages:
                    st.session_state[f"page_{category}"] += 1
