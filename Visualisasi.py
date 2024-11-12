import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca dataset yang sudah dibersihkan
data = pd.read_csv('data_with_sentiment_and_pestel.csv')

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Tampilkan dataset
st.write("Tabel Data Analisis:")
st.dataframe(data)

 # Tampilkan distribusi sentimen
    st.write("Distribusi Sentimen:")
    sentiment_counts = data['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', color=['green', 'blue'], ax=ax)
    ax.set_title("Distribusi Sentimen")
    ax.set_xlabel("Sentimen")
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

# Visualisasi PESTEL dan Sentimen
    st.write("Distribusi Sentimen Berdasarkan Kategori PESTEL:")
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    sns.countplot(data=data, x='PESTEL_Category', hue='Sentiment', palette='viridis')
    plt.title("Distribusi Sentimen Berdasarkan Kategori PESTEL")
    plt.xlabel("Kategori PESTEL")
    plt.ylabel("Jumlah")
    plt.legend(title="Sentimen")
    st.pyplot(plt.gcf())  # Menampilkan plot pada Streamlit
