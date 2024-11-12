import streamlit as st
import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membersihkan teks
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Mengganti spasi ganda dengan satu spasi
    text = re.sub(r'[^\w\s.,]', '', text)  # Menghapus karakter yang bukan kata, spasi, koma, atau titik
    return text.strip()

# Fungsi untuk mengkategorikan berita menggunakan analisis PESTEL
def categorize_pestel(summary):
    summary = summary.lower()
    if any(keyword in summary for keyword in ["politik", "pemilu", "kebijakan pemerintah", "regulasi", "presiden", "menteri"]):
        return "Political"
    elif any(keyword in summary for keyword in ["ekonomi", "pendapatan", "inflasi", "keuangan", "pasar", "industri"]):
        return "Economic"
    elif any(keyword in summary for keyword in ["masyarakat", "sosial", "budaya", "komunitas", "pendidikan", "kesehatan"]):
        return "Social"
    elif any(keyword in summary for keyword in ["teknologi", "inovasi", "internet", "digital", "perangkat", "sistem"]):
        return "Technological"
    elif any(keyword in summary for keyword in ["lingkungan", "hutan", "polusi", "iklim", "banjir", "bencana"]):
        return "Environmental"
    elif any(keyword in summary for keyword in ["hukum", "peraturan", "legal", "undang-undang", "izin", "pengadilan"]):
        return "Legal"
    else:
        return "Social"  # Kategori default jika tidak ada kecocokan

# Fungsi untuk menentukan sentimen dari teks
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return 'Positif' if sentiment_score > 0 else 'Netral'

# Set judul aplikasi
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Memuat file CSV
uploaded_file = st.file_uploader("Upload file CSV", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    
    # Membersihkan teks pada kolom 'title' dan 'summary'
    data['title'] = data['title'].fillna('').apply(clean_text)
    data['summary'] = data['summary'].fillna('').apply(clean_text)
    
    # Mengkategorikan PESTEL dan menganalisis sentimen
    data['PESTEL_Category'] = data['summary'].apply(categorize_pestel)
    data['Sentiment'] = data['summary'].apply(get_sentiment)
    
    # Tampilkan data setelah proses
    st.write("Data setelah diproses:")
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
    
    # Menyediakan pilihan untuk mengunduh hasil analisis
    st.write("Download hasil analisis:")
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name='data_with_sentiment_and_pestel.csv', mime='text/csv')
