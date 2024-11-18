import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset bawaan (contoh dataset, ganti dengan data Anda sendiri)
data = pd.DataFrame({
    'Sentiment': ['Positive', 'Neutral', 'Positive', 'Neutral', 'Positive', 'Neutral'],
    'PESTEL_Category': ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal'],
    'Detail': [
        "Kebijakan baru pemerintah mendukung energi terbarukan.",
        "Ekonomi global memengaruhi biaya investasi PLN.",
        "Proyek inovasi baru meningkatkan efisiensi energi.",
        "Teknologi smart grid masih memerlukan pengembangan.",
        "Upaya keberlanjutan lingkungan berjalan sukses.",
        "Perubahan regulasi memberikan tantangan baru."
    ]
})

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
selected_sentiment = st.radio("Pilih Sentimen", options=['Positive', 'Neutral'])

# Filter data berdasarkan sentimen yang dipilih
filtered_data = data[data['Sentiment'] == selected_sentiment]

# Tampilkan data yang difilter
st.write(f"Data dengan Sentimen **{selected_sentiment}**:")
st.dataframe(filtered_data)
