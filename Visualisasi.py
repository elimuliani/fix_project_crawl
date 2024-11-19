import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset dari file CSV
uploaded_file = "data_with_sentiment_and_pestel.csv"

if uploaded_file:
    # Membaca dataset
    data = pd.read_csv(uploaded_file)

    # Memperbaiki penulisan salah ketik di kolom 'PESTEL_Category'
    data['PESTEL_Category'] = data['PESTEL_Category'].replace({'Environtmental': 'Environmental'})

    # Urutan kategori PESTEL
    pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']

    # Tampilkan jumlah total data
    total_data = len(data)
    st.write(f"Total Jumlah Data: {total_data} baris")

    # Tampilkan dataset
    st.write("Tabel Data Analisis:")
    st.dataframe(data)

    # Tampilkan distribusi sentimen
    st.write("Distribusi Sentimen:")
    sentiment_counts = data['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', color=['green', 'gray', 'blue'], ax=ax)
    ax.set_title("Distribusi Sentimen")
    ax.set_xlabel("Sentimen")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

    # Filter data berdasarkan sentimen
    st.write("Klik untuk melihat data berdasarkan Sentimen:")
    selected_sentiment = st.radio("Pilih Sentimen", options=data['Sentiment'].unique())
    filtered_data = data[data['Sentiment'] == selected_sentiment]
    st.write(f"Data dengan Sentimen *{selected_sentiment}*:")
    st.dataframe(filtered_data, use_container_width=True)

    # Filter data berdasarkan kategori PESTEL
    st.write("Klik untuk melihat data berdasarkan Kategori PESTEL:")
    selected_pestel = st.selectbox("Pilih Kategori PESTEL", options=pestel_order)
    pestel_filtered_data = data[data['PESTEL_Category'] == selected_pestel]
    sentiment_in_pestel = pestel_filtered_data['Sentiment'].unique()
    st.write(f"Kategori PESTEL *{selected_pestel}* terkait dengan Sentimen: {', '.join(sentiment_in_pestel)}")
    st.dataframe(pestel_filtered_data, use_container_width=True)

    # Pie Chart Interaktif untuk PESTEL
    st.write("Distribusi Berita berdasarkan Kategori PESTEL:")

    # Menghitung jumlah setiap kategori PESTEL, termasuk yang tidak ada data
    pestel_counts = data['PESTEL_Category'].value_counts().reindex(pestel_order, fill_value=0).reset_index()
    pestel_counts.columns = ['PESTEL_Category', 'Jumlah']

    # Membuat Pie Chart setelah perbaikan
    fig_pie = px.pie(
        pestel_counts,
        names='PESTEL_Category',
        values='Jumlah',
        color='PESTEL_Category',
        category_orders={'PESTEL_Category': pestel_order},  # Urutkan sesuai PESTEL
        color_discrete_sequence=px.colors.qualitative.Set3,  # Warna menarik
        title="Distribusi Berita PESTEL"
    )
    st.plotly_chart(fig_pie)

else:
    st.error("File CSV tidak ditemukan. Silakan unggah file yang sesuai.")
