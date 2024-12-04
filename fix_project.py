import streamlit as st
import pandas as pd

# Load file CSV
try:
    data = pd.read_csv('pln_clean.csv')
    st.write("File CSV berhasil dimuat.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat file CSV: {e}")
    st.stop()

# Periksa apakah kolom yang dibutuhkan ada
required_columns = ['headline', 'link', 'category', 'Sentiment']
for col in required_columns:
    if col not in data.columns:
        st.error(f"Kolom '{col}' tidak ditemukan dalam file CSV.")
        st.stop()

# Pastikan tidak ada data kosong
data['headline'] = data['headline'].fillna('Judul Tidak Tersedia')
data['link'] = data['link'].fillna('#')
data['category'] = data['PESTEL_Category'].fillna('Tidak Dikategorikan')
data['Sentiment'] = data['Sentiment'].fillna('Netral')

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Beranda", "Berita dan Kategori", "Distribusi PESTEL & Sentimen"]
)

# Halaman Beranda
if menu == "Beranda":
    st.title("📊 Analisis PESTEL dan Sentimen")
    st.markdown("""
        Selamat datang di dashboard analisis berita PLN berdasarkan kategori **PESTEL** dan **Sentimen**.
    """)

# Halaman Berita dan Kategori
elif menu == "Berita dan Kategori":
    st.title("📜 Daftar Berita")
    st.markdown("Klik judul berita untuk membaca lebih lanjut.")
    for i, row in data.iterrows():
        st.markdown(f"#### [{row['headline']}]({row['link']})")
        st.markdown(f"**Kategori:** {row['PESTEL_Category']} | **Sentimen:** {row['Sentiment']}")
        st.markdown("---")

# Halaman Distribusi
elif menu == "Distribusi PESTEL & Sentimen":
    st.title("📊 Distribusi PESTEL dan Sentimen")
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Plot
    plt.figure(figsize=(10, 6))
    sns.countplot(
        data=data,
        x='Category',
        hue='Sentiment',
        order=['Politik', 'Ekonomi', 'Sosial', 'Teknologi', 'Lingkungan', 'Legal'],
        palette='viridis'
    )
    plt.title('Distribusi Sentimen berdasarkan Kategori PESTEL', fontsize=16)
    plt.xlabel('Kategori PESTEL', fontsize=12)
    plt.ylabel('Jumlah', fontsize=12)
    plt.legend(title='Sentimen')
    plt.xticks(rotation=45)
    st.pyplot(plt)
