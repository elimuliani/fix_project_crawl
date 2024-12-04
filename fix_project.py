import streamlit as st
import pandas as pd

# Set page config harus dipanggil di awal
st.set_page_config(page_title="Analisis PESTEL & Sentimen", layout="wide")

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

# Pastikan tidak ada data kosong dan sesuaikan kolom
data['headline'] = data['headline'].fillna('Judul Tidak Tersedia')
data['link'] = data['link'].fillna('#')
data['category'] = data['category'].fillna('Tidak Dikategorikan')  # Menggunakan 'category' bukan 'PESTEL_Category'
data['Sentiment'] = data['Sentiment'].fillna('Netral')

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Beranda", "Berita dan Kategori", "Distribusi PESTEL & Sentimen"],
    index=0,  # Set default menu ke "Beranda"
    label_visibility="collapsed"  # Menyembunyikan label untuk tampilan lebih bersih
)

# Mengatur tema dan layout untuk lebih bersih dan nyaman
st.markdown(
    """
    <style>
    .css-18e3th9 {
        font-size: 20px;
        font-weight: bold;
    }
    .css-1v3fvcr {
        font-size: 16px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Halaman Beranda
if menu == "Beranda":
    st.title("📊 Analisis PESTEL dan Sentimen")
    st.markdown("""
        Selamat datang di dashboard analisis berita PLN berdasarkan kategori **PESTEL** dan **Sentimen**.
        Pilih menu di sidebar untuk mulai menjelajah.
    """)

# Halaman Berita dan Kategori
elif menu == "Berita dan Kategori":
    st.title("📜 Daftar Berita")
    st.markdown("Klik judul berita untuk membaca lebih lanjut.")
    st.write("")

    # Display berita dengan layout yang rapi dan bersih
    for i, row in data.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"#### [{row['headline']}]({row['link']})")
        with col2:
            st.markdown(f"**Kategori:** {row['category']} | **Sentimen:** {row['Sentiment']}")
        st.markdown("---")

# Halaman Distribusi PESTEL & Sentimen
elif menu == "Distribusi PESTEL & Sentimen":
    st.title("📊 Distribusi PESTEL dan Sentimen")
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Menambahkan padding dan mengatur ukuran tampilan plot agar lebih nyaman
    plt.figure(figsize=(12, 7))
    sns.countplot(
        data=data,
        x='category',  # Pastikan ini sesuai dengan kolom yang benar yaitu 'category'
        hue='Sentiment',
        order=['Politik', 'Ekonomi', 'Sosial', 'Teknologi', 'Lingkungan', 'Legal'],
        palette='viridis'
    )
    plt.title('Distribusi Sentimen berdasarkan Kategori PESTEL', fontsize=16)
    plt.xlabel('Kategori PESTEL', fontsize=12)
    plt.ylabel('Jumlah', fontsize=12)
    plt.legend(title='Sentimen', loc='upper right', fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    st.pyplot(plt)
