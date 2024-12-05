import streamlit as st
import pandas as pd
import plotly.express as px

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

# PESTEL categories in correct order
categories_order = [
    "Politik", "Ekonomi", "Sosial", "Teknologi", "Lingkungan", "Legal"
]

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

# Dictionary to store the count of news for each category
category_counts = {category: 0 for category in categories_order}

# Dropdown untuk memilih kategori dari pie chart
selected_pestel_category = st.sidebar.selectbox(
    "Pilih Kategori PESTEL untuk Fokus:",
    options=["Semua"] + categories_order,
)

# Display each category and its clickable headlines with pagination
items_per_page = 5  # Number of items per page

for i, category in enumerate(categories_order):
    if selected_pestel_category != "Semua" and selected_pestel_category != category:
        continue  # Skip rendering this category if it does not match the selected category

    with cols[i % len(cols)]:
        color = categories[category]
        st.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 10px;'>"
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

            # If there are multiple pages, display navigation
            if total_pages > 1:
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button("←", key=f"prev_{category}", help="Halaman Sebelumnya", use_container_width=True):
                        if current_page > 1:
                            st.session_state[f"page_{category}"] -= 1  # Go to previous page

                with col2:
                    if st.button("→", key=f"next_{category}", help="Halaman Berikutnya", use_container_width=True):
                        if current_page < total_pages:
                            st.session_state[f"page_{category}"] += 1  # Go to next page

                # Display the current page number
                st.markdown(
                    f"<div style='text-align: center; font-size: 10px; color: gray;'>Halaman {current_page}/{total_pages}</div>",
                    unsafe_allow_html=True,
                )

# Create and display the interactive pie chart showing the percentage of news per category
# Ensure categories are in the correct order
sorted_category_counts = {category: category_counts[category] for category in categories_order}

fig = px.pie(
    names=list(sorted_category_counts.keys()),
    values=list(sorted_category_counts.values()),
    color=list(sorted_category_counts.keys()),
    color_discrete_map=categories,
    title="Distribusi Kategori Berita",
    hole=0.3,  # Donut chart for better visibility
)

# Update layout for better readability
fig.update_layout(
    legend_title="Kategori",
    margin=dict(t=20, b=10, l=10, r=10),  # Reduce unnecessary margin
    height=350,  # Adjust height for compactness
    title_x=0.5,  # Center the title
)

# Display the interactive pie chart
st.plotly_chart(fig, use_container_width=True)
