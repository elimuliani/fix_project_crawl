import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

if uploaded_file:
    # Membaca dataset
    data = pd.read_csv(uploaded_file)

    st.write("Tabel Data Analisis:")
    st.dataframe(data)

    # Visualisasi Distribusi Sentimen
    st.write("Distribusi Sentimen Berita:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=data, x='Sentiment', palette='coolwarm', ax=ax)
    ax.set_title("Distribusi Sentimen Berita", fontsize=16)
    ax.set_xlabel("Kategori Sentimen", fontsize=14)
    ax.set_ylabel("Jumlah", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    st.pyplot(fig)

    # Visualisasi Distribusi PESTEL dan Sentimen
    st.write("Distribusi Sentimen berdasarkan Kategori PESTEL:")
    fig, ax = plt.subplots(figsize=(12, 7))
    pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']
    sns.countplot(
        data=data,
        x='PESTEL_Category',
        hue='Sentiment',
        order=pestel_order,
        palette='coolwarm',
        ax=ax
    )
    ax.set_title('Distribusi Sentimen berdasarkan Kategori PESTEL', fontsize=16)
    ax.set_xlabel('Kategori PESTEL', fontsize=14)
    ax.set_ylabel('Jumlah', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    ax.legend(title='Sentimen', fontsize=12)
    st.pyplot(fig)

    # Pie Chart Interaktif PESTEL
    st.write("Distribusi Berita berdasarkan Kategori PESTEL:")
    pestel_counts = data['PESTEL_Category'].value_counts().reset_index()
    pestel_counts.columns = ['PESTEL_Category', 'Jumlah']

    # Buat pie chart menggunakan Plotly
    fig_pie = px.pie(
        pestel_counts, 
        names='PESTEL_Category', 
        values='Jumlah', 
        color='PESTEL_Category',
        color_discrete_sequence=px.colors.qualitative.Set2,  # Warna yang menarik
        title="Distribusi Berita PESTEL"
    )

    # Tambahkan tautan interaktif
    fig_pie.update_traces(
        hoverinfo="label+percent+value",
        textinfo="label+percent",
        pull=[0.1 if i == 0 else 0 for i in range(len(pestel_counts))],  # Highlight satu kategori
    )

    # Tampilkan grafik pie chart
    st.plotly_chart(fig_pie)

    # Klik pada kategori PESTEL untuk melihat berita
    selected_category = st.selectbox("Pilih Kategori PESTEL untuk melihat berita terkait:", pestel_counts['PESTEL_Category'])
    filtered_data = data[data['PESTEL_Category'] == selected_category]

    st.write(f"Berita terkait kategori *{selected_category}*:")
    st.dataframe(filtered_data[['Title', 'Link']], use_container_width=True)

    st.write("Klik tautan di kolom 'Link' untuk membaca berita.")
else:
    st.error("Silakan unggah file CSV untuk memulai analisis.")
