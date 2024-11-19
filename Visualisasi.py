import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset dari file CSV
uploaded_file = "data_with_sentiment_and_pestel.csv"

if uploaded_file:
    # Membaca file CSV
    data = pd.read_csv(uploaded_file)
    
    # Tampilkan dataset
    st.write("Tabel Data Analisis:")
    st.dataframe(data)
    
    # Visualisasi Distribusi Sentimen
    st.write("Distribusi Sentimen Berita:")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x='Sentiment', palette='viridis', ax=ax)
    ax.set_title("Distribusi Sentimen Berita")
    ax.set_xlabel("Kategori Sentimen")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

    # Visualisasi Distribusi PESTEL dan Sentimen
    st.write("Distribusi Sentimen berdasarkan Kategori PESTEL:")
    fig, ax = plt.subplots(figsize=(10, 6))
    pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']  # Urutan kategori PESTEL
    sns.countplot(
        data=data,
        x='PESTEL_Category',
        hue='Sentiment',
        order=pestel_order,
        palette='viridis',
        ax=ax
    )
    ax.set_title('Distribusi Sentimen berdasarkan Kategori PESTEL')
    ax.set_xlabel('Kategori PESTEL')
    ax.set_ylabel('Jumlah')
    plt.xticks(rotation=45)
    plt.legend(title='Sentimen', loc='upper right')
    st.pyplot(fig)
else:
    st.error("File CSV tidak ditemukan. Silakan unggah file yang sesuai.")
