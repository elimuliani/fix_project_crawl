import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset bawaan
# Ganti dengan path file lokal atau buat dataset langsung di sini
# Contoh dataset bawaan
data = pd.DataFrame({
    'Sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative', 'Positive', 'Negative'],
    'PESTEL_Category': ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal', 'Economic']
})

# Tampilkan dataset
st.write("Tabel Data Analisis:")
st.dataframe(data)

# Tampilkan distribusi sentimen
st.write("Distribusi Sentimen:")
sentiment_counts = data['Sentiment'].value_counts()
fig, ax = plt.subplots()
sentiment_counts.plot(kind='bar', color=['green', 'blue', 'gray'], ax=ax)
ax.set_title("Distribusi Sentimen")
ax.set_xlabel("Sentimen")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

# Visualisasi PESTEL dan Sentimen
# Define the custom order for PESTEL categories
pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']
st.write("Distribusi Sentimen Berdasarkan Kategori PESTEL:")
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
sns.countplot(data=data, x='PESTEL_Category', hue='Sentiment', palette='viridis', order=pestel_order)
plt.title("Distribusi Sentimen Berdasarkan Kategori PESTEL")
plt.xlabel("Kategori PESTEL")
plt.ylabel("Jumlah")
plt.legend(title="Sentimen")
st.pyplot(plt.gcf())  # Menampilkan plot pada Streamlit
