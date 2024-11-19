import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset dari file CSV
uploaded_file = "data_with_sentiment_and_pestel.csv"

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    
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
else:
    st.error("File CSV tidak ditemukan. Silakan unggah file yang sesuai.")
