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
file_path = "pln_clean_fix.csv"  # Ganti dengan nama file CSV Anda
try:
    data = pd.read_csv(file_path)
    st.success("Data berhasil dimuat!")
except FileNotFoundError:
    st.error("File CSV tidak ditemukan. Pastikan file berada di path yang benar.")
    st.stop()
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.stop()

# Ensure the required columns exist
required_columns = {"headline", "link", "category", "date"}
if not required_columns.issubset(data.columns):
    st.error(f"File CSV harus memiliki kolom: {required_columns}")
    st.stop()

# Convert date column to datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['formatted_date'] = data['date'].dt.strftime('%d-%m-%Y')

# Drop rows with invalid dates
data = data.dropna(subset=['date'])

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

# Display each category and its clickable headlines with pagination
items_per_page = 5  # Number of items per page

# Display the category headlines and their data
for i, category in enumerate(categories_order):
    with cols[i]:
        color = categories[category]
        category_data = data[data["category"] == category]

        # Display category header with count of news
        count = len(category_data)
        st.markdown(f"""
        <div class="category-header" style='background: {color}; padding: 10px; border-radius: 10px;'>
            <h4 style='text-align: center; color: white;'>{category}</h4>
            <p style='text-align: center; color: white; font-size: 14px;'>({count} berita)</p>
        </div>
        """, unsafe_allow_html=True)

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
                date = row["formatted_date"]  # Use formatted date
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <a href="{link}" target="_blank" style="text-decoration: none; color: black;">
                        <h5>{headline}</h5>
                    </a>
                    <p style="color: gray; font-size: 16px;">{date}</p>
                </div>
                """, unsafe_allow_html=True)

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

# Pie Chart
pestel_counts = data['category'].value_counts().reindex(categories_order, fill_value=0).reset_index()
pestel_counts.columns = ['PESTEL_Category', 'Jumlah']

# Create pie chart
fig_pie = px.pie(
    pestel_counts,
    names='PESTEL_Category',
    values='Jumlah',
    color='PESTEL_Category',
    category_orders={'PESTEL_Category': categories_order},
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="Pie Chart Berita PESTEL"
)

# Display pie chart with percentage
st.plotly_chart(fig_pie)

# Rekomendasi Pembelajaran
st.markdown("""
<div style='padding: 20px; background-color: #f9f9f9; border-radius: 10px; margin-top: 20px;'>
    <h3 style='text-align: center;'>📘 Rekomendasi Generate AI untuk Kompetensi Masa Depan</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">🌐 Political (Politik)</h4>
            <ul>
                <li>Mengelola Hubungan Multi-Stakeholder dalam Proyek Infrastruktur Strategis</li>
                <li>Advokasi Kebijakan untuk Transisi Energi Berkelanjutan</li>
            </ul>
        </div>
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">💰 Economic (Ekonomi)</h4>
            <ul>
                <li>Model Bisnis untuk Green Energy</li>
                <li>Ekonomi Sirkular dan Manajemen Risiko Energi</li>
            </ul>
        </div>
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">🤝 Social (Sosial)</h4>
            <ul>
                <li>Strategi Sosialisasi dan Edukasi Energi Baru Terbarukan</li>
                <li>Pemberdayaan Ekonomi Lokal melalui Infrastruktur Energi</li>
            </ul>
        </div>
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">🔧 Technological (Teknologi)</h4>
            <ul>
                <li>IoT dan Smart Grid untuk Infrastruktur Kelistrikan</li>
                <li>Pengembangan Kompetensi Hidrogen dan Kendaraan Listrik</li>
            </ul>
        </div>
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">🌱 Environmental (Lingkungan)</h4>
            <ul>
                <li>Perencanaan Infrastruktur Hijau untuk Ketahanan Energi</li>
                <li>Manajemen Risiko Bencana pada Infrastruktur Energi</li>
            </ul>
        </div>
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">⚖ Legal (Hukum)</h4>
            <ul>
                <li>Hukum Energi dan Standar Internasional</li>
                <li>Manajemen Risiko Hukum dalam Transisi Energi</li>
            </ul>
        </div>
        <div style="background-color: #eef7ff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h4 style="color: #2b6cb0;">🚀 Future Competencies</h4>
            <ul>
                <li>Green Leadership untuk Manajemen Proyek Energi</li>
                <li>Multidisiplin Skill untuk Inovasi Energi</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

