import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset dari file CSV
uploaded_file = "data_with_sentiment_and_pestel.csv"

if uploaded_file:
    # Membaca dataset
    data = pd.read_csv(uploaded_file)
    
    # Tampilkan jumlah total data yang dimiliki
    total_data = len(data)
    st.write(f"Total Jumlah Data: {total_data} baris")
    
    # Tampilkan dataset
    st.write("Tabel Data Analisis:")
    st.dataframe(data)
    
    # Tampilkan distribusi sentimen
    st.write("Distribusi Sentimen:")
    sentiment_counts = data['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', color=['green', 'gray'], ax=ax)
    ax.set_title("Distribusi Sentimen")
    ax.set_xlabel("Sentimen")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

    # Pilihan untuk melihat data berdasarkan sentimen
    st.write("Klik untuk melihat data berdasarkan Sentimen:")
    selected_sentiment = st.radio("Pilih Sentimen", options=data['Sentiment'].unique())

    # Filter data berdasarkan sentimen yang dipilih
    filtered_data = data[data['Sentiment'] == selected_sentiment]

    # Tampilkan data yang difilter
    st.write(f"Data dengan Sentimen *{selected_sentiment}*:")
    st.dataframe(filtered_data, use_container_width=True)  # Menampilkan seluruh data yang difilter

    # Pilihan untuk melihat data berdasarkan kategori PESTEL
    st.write("Klik untuk melihat data berdasarkan Kategori PESTEL:")
    selected_pestel = st.selectbox("Pilih Kategori PESTEL", options=data['PESTEL_Category'].unique())

    # Filter data berdasarkan kategori PESTEL
    pestel_filtered_data = data[data['PESTEL_Category'] == selected_pestel]

    # Identifikasi sentimen terkait PESTEL
    sentiment_in_pestel = pestel_filtered_data['Sentiment'].unique()

    # Tampilkan data yang difilter dan sentimen terkait
    st.write(f"Data dengan Kategori PESTEL *{selected_pestel}*:")
    st.dataframe(pestel_filtered_data, use_container_width=True)  # Menampilkan seluruh data terkait kategori PESTEL
    st.write(f"Kategori PESTEL *{selected_pestel}* terkait dengan Sentimen: {', '.join(sentiment_in_pestel)}")

    # Pie Chart Interaktif
    st.write("Distribusi Berita berdasarkan Kategori PESTEL:")
    pestel_counts = data['PESTEL_Category'].value_counts().reset_index()
    pestel_counts.columns = ['PESTEL_Category', 'Jumlah']

    # Urutan kategori PESTEL
    pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']

    # Buat pie chart menggunakan Plotly
    fig_pie = px.pie(
        pestel_counts,
        names='PESTEL_Category',
        values='Jumlah',
        color='PESTEL_Category',
        category_orders={'PESTEL_Category': pestel_order},  # Urutkan sesuai PESTEL
        color_discrete_sequence=px.colors.qualitative.Set3,  # Warna menarik
        title="Distribusi Berita PESTEL"
    )

    # Tampilkan grafik pie chart
    st.plotly_chart(fig_pie)

    # Klik pada kategori PESTEL untuk melihat berita
    selected_pie_category = st.selectbox("Pilih Kategori PESTEL untuk melihat data terkait:", pestel_order)
    pie_filtered_data = data[data['PESTEL_Category'] == selected_pie_category]

    st.write(f"Data dengan Kategori PESTEL *{selected_pie_category}*:")
    st.dataframe(pie_filtered_data, use_container_width=True)

else:
    st.error("File CSV tidak ditemukan. Silakan unggah file yang sesuai.")
