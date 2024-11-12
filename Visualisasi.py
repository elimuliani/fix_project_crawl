import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Unggah file CSV
uploaded_file = st.file_uploader("Upload file CSV", type="csv")

if uploaded_file is not None:
    # Membaca dataset yang diunggah
    data = pd.read_csv(uploaded_file)
    
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

else:
    st.write("Silakan unggah file CSV untuk melihat analisis.")
