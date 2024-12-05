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

# Display each category and its clickable headlines with pagination
items_per_page = 5  # Number of items per page

# Display the category headlines and their data
for i, category in enumerate(categories_order):
    with cols[i]:
        color = categories[category]
        st.markdown(f"""
        <div class="category-header" style='background: {color}; padding: 10px; border-radius: 10px;'>
            <h4 style='text-align: center; color: white;'>{category}</h4>
        </div>
        """, unsafe_allow_html=True)

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

            # Display paginated headlines as cards
            for _, row in page_data.iterrows():
                headline = row["headline"]
                link = row["link"]
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <a href="{link}" target="_blank" style="text-decoration: none; color: black;">
                        <h5>{headline}</h5>
                    </a>
                </div>
                """, unsafe_allow_html=True)

            # Update the category count based on the number of items displayed on this page
            category_counts[category] += len(page_data)

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

# Menghitung jumlah berita per kategori sesuai urutan PESTEL
category_counts = data['category'].value_counts().reindex(categories_order, fill_value=0)

# Membuat pie chart
fig = px.pie(
    names=categories_order,  # Sesuai urutan PESTEL
    values=category_counts,  # Nilai jumlah berita
    color=categories_order,  # Warna sesuai kategori
    title="Distribusi Kategori Berita (PESTEL)",
    hole=0.3,  # Membuat donut chart
    color_discrete_map={
        "Politik": "#FFD700",   # Kuning
        "Ekonomi": "#32CD32",   # Hijau
        "Sosial": "#1E90FF",    # Biru
        "Teknologi": "#8A2BE2", # Ungu
        "Lingkungan": "#FF6347",# Merah
        "Legal": "#FF4500",     # Jingga
    }
)

# Mengatur tata letak agar lebih jelas
fig.update_traces(
    hoverinfo="label+percent",
    textinfo="label+value",
    pull=[0.1 if value > 0 else 0 for value in category_counts]
)

fig.update_layout(
    showlegend=True,
    legend_title="Kategori",
    legend=dict(
        orientation="h",  # Horizontal
        yanchor="bottom",
        y=-0.2,  # Menempatkan legenda di bawah chart
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=40, b=40, l=40, r=40),  # Margin agar lebih jelas
    height=500,  # Tinggi chart
    title_x=0.5,  # Judul di tengah
    title_font=dict(size=16),
)

# Menampilkan pie chart
st.plotly_chart(fig)
