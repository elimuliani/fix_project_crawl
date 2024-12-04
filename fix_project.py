import streamlit as st
import pandas as pd

# Load data
data = pd.read_csv('pln_clean.csv')

# Title and Description
st.set_page_config(page_title="Analisis PESTEL PLN", layout="wide")
st.title("📊 Analisis Kategori PESTEL dan Sentimen")
st.markdown("""
    Selamat datang di dashboard analisis berita PLN berdasarkan kategori **PESTEL** dan **sentimen**.
    Informasi dirancang dengan tata letak yang sederhana, rapi, dan mudah dipahami.
""")

# Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Beranda", "Berita dan Kategori", "Distribusi PESTEL & Sentimen"]
)

# Halaman 1: Beranda
if menu == "Beranda":
    st.header("Beranda")
    st.markdown("""
        Dashboard ini memberikan wawasan terkait:
        - Kategori **PESTEL** dari berita terkait PLN.
        - Analisis sentimen berita (Positif/Netral).
        - Distribusi berita berdasarkan kategori.
        
        **Petunjuk Penggunaan:**
        - Gunakan menu navigasi di sebelah kiri untuk berpindah halaman.
        - Klik judul berita untuk membaca detailnya.
    """)

# Halaman 2: Berita dan Kategori
elif menu == "Berita dan Kategori":
    st.header("📜 Daftar Berita berdasarkan PESTEL")
    st.markdown("Klik judul berita untuk membaca lebih lanjut.")
    
    # Tampilkan data dalam card layout
    for i, row in data.iterrows():
        with st.container():
            st.markdown(f"#### [{row['headline']}]({row['link']})")
            st.markdown(f"**Kategori:** {row['PESTEL_Category']} | **Sentimen:** {row['Sentiment']}")
            st.markdown("---")

# Halaman 3: Distribusi PESTEL dan Sentimen
elif menu == "Distribusi PESTEL & Sentimen":
    st.header("📊 Distribusi Kategori PESTEL dan Sentimen")
    st.markdown("Visualisasi distribusi kategori **PESTEL** berdasarkan sentimen.")

    # Load visualization libraries
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Sort PESTEL categories for better readability
    pestel_order = ['Politik', 'Ekonomi', 'Sosial', 'Teknologi', 'Lingkungan', 'Legal']

    # Plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.countplot(
        data=data,
        x='PESTEL_Category',
        hue='Sentiment',
        order=pestel_order,
        palette='viridis'
    )
    plt.title('Distribusi Sentimen berdasarkan Kategori PESTEL', fontsize=16)
    plt.xlabel('Kategori PESTEL', fontsize=12)
    plt.ylabel('Jumlah', fontsize=12)
    plt.legend(title='Sentimen')
    plt.xticks(rotation=45)
    
    # Show plot
    st.pyplot(plt)

    st.markdown("Analisis ini membantu memahami distribusi berita dan sentimennya di berbagai kategori PESTEL.")

# Footer
st.markdown("""
    ---
    **Dashboard Analisis PESTEL**  
    Dibuat untuk mempermudah analisis berita PLN dengan tata letak sederhana dan ramah pengguna.
""")
