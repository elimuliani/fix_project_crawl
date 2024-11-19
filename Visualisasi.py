import streamlit as st
import pandas as pd
import plotly.express as px

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset dari file CSV
uploaded_file = "data_with_sentiment_and_pestel.csv"

if uploaded_file:
    # Membaca dataset
    data = pd.read_csv(uploaded_file)

    # Tampilkan jumlah total data
    total_data = len(data)
    st.write(f"Total Jumlah Data: {total_data} baris")

    # Urutan kategori PESTEL
    pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']

    # Pilihan untuk melihat data berdasarkan kategori PESTEL
    st.write("Klik untuk melihat data berdasarkan Kategori PESTEL yang berurutan:")
    selected_pestel = st.selectbox("Pilih Kategori PESTEL", options=pestel_order)

    # Filter data berdasarkan kategori PESTEL
    pestel_filtered_data = data[data['PESTEL_Category'] == selected_pestel]

    # Identifikasi sentimen terkait PESTEL
    sentiment_in_pestel = pestel_filtered_data['Sentiment'].unique()

    # Tampilkan data kategori PESTEL dan sentimen terkait
    st.write(f"Kategori PESTEL *{selected_pestel}* terkait dengan Sentimen: {', '.join(sentiment_in_pestel)}")

else:
    st.error("File CSV tidak ditemukan. Silakan unggah file yang sesuai.")
