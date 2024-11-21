import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

# Judul aplikasi web
st.title("Analisis PESTEL dan Sentimen Berita PLN")

# Membaca dataset dari file CSV yang sudah ada (misalnya, data.csv atau data di bawah)
# Contoh data buatan sebagai pengganti upload file CSV
data = pd.DataFrame({
    'title': ['Masalah listrik padam', 'Gangguan jaringan', 'Pemadaman berkepanjangan', 'Kerusakan alat listrik', 'Listrik tidak stabil', 'Gangguan aliran listrik', 'Perbaikan sistem listrik', 'Masalah alat pemutus', 'Gangguan komunikasi', 'Overload sistem'],
    'PESTEL_Category': ['Technological', 'Technological', 'Economic', 'Legal', 'Social', 'Environmental', 'Political', 'Economic', 'Legal', 'Social'],
    'Sentiment': ['Negative', 'Negative', 'Neutral', 'Negative', 'Positive', 'Neutral', 'Positive', 'Negative', 'Neutral', 'Positive'],
    'pub_date': pd.to_datetime(['2024-11-20', '2024-11-19', '2024-11-18', '2024-11-17', '2024-11-16', '2024-11-15', '2024-11-14', '2024-11-13', '2024-11-12', '2024-11-11'])
})

# Urutan kategori PESTEL
pestel_order = ['Political', 'Economic', 'Social', 'Technological', 'Environmental', 'Legal']

# Tampilkan jumlah total data
total_data = len(data)
st.write(f"Total Jumlah Data: {total_data} baris")

# Tampilkan distribusi sentimen
st.write("Distribusi Sentimen:")
sentiment_counts = data['Sentiment'].value_counts()
fig, ax = plt.subplots()
sentiment_counts.plot(kind='bar', color=['green', 'gray', 'blue'], ax=ax)
ax.set_title("Distribusi Sentimen")
ax.set_xlabel("Sentimen")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

# Filter data berdasarkan sentimen
st.write("Klik untuk melihat data berdasarkan Sentimen:")
selected_sentiment = st.radio("Pilih Sentimen", options=data['Sentiment'].unique())
filtered_data = data[data['Sentiment'] == selected_sentiment]
st.write(f"Data dengan Sentimen *{selected_sentiment}*:")
st.dataframe(filtered_data, use_container_width=True)

# Filter data berdasarkan kategori PESTEL
st.write("Klik untuk melihat data berdasarkan Kategori PESTEL:")
selected_pestel = st.selectbox("Pilih Kategori PESTEL", options=pestel_order)
pestel_filtered_data = data[data['PESTEL_Category'] == selected_pestel]
sentiment_in_pestel = pestel_filtered_data['Sentiment'].unique()
st.write(f"Kategori PESTEL *{selected_pestel}* terkait dengan Sentimen: {', '.join(sentiment_in_pestel)}")
st.dataframe(pestel_filtered_data, use_container_width=True)

# Pie Chart Interaktif untuk PESTEL
st.write("Distribusi Berita berdasarkan Kategori PESTEL:")
pestel_counts = data['PESTEL_Category'].value_counts().reindex(pestel_order, fill_value=0).reset_index()
pestel_counts.columns = ['PESTEL_Category', 'Jumlah']
fig_pie = px.pie(
    pestel_counts,
    names='PESTEL_Category',
    values='Jumlah',
    color='PESTEL_Category',
    category_orders={'PESTEL_Category': pestel_order},
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="Distribusi Berita PESTEL"
)
st.plotly_chart(fig_pie)

# **Tampilan "Top Problems" dalam Bentuk Tabel yang Menarik:**

st.subheader("Masalah Utama yang Dilaporkan")

# Mendapatkan 10 masalah utama
top_problems = data['title'].value_counts().head(10)

# Menampilkan tabel dalam layout kolom kiri-kanan
col1, col2 = st.columns([2, 1])

with col1:
    # Menampilkan tabel dengan styling
    st.write("Tabel Top 10 Masalah Utama:")
    top_problems_df = top_problems.reset_index()
    top_problems_df.columns = ['Masalah', 'Jumlah']
    st.dataframe(top_problems_df.style.format({'Jumlah': '{:,}'}).background_gradient(axis=0, cmap='YlGnBu'))

with col2:
    # Menampilkan visualisasi bar chart untuk top problems
    st.write("Grafik Masalah Utama:")
    fig, ax = plt.subplots(figsize=(8, 5))
    top_problems.plot(kind='bar', color='purple', ax=ax)
    ax.set_title('Top 10 Masalah Utama')
    ax.set_xlabel('Masalah')
    ax.set_ylabel('Jumlah')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

# Word Cloud untuk masalah utama
if 'title' in data.columns:
    all_problems = ' '.join(data['title'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(all_problems)
    st.write("Word Cloud untuk Masalah Utama:")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Analisis laporan berdasarkan jam dan hari
if 'pub_date' in data.columns:
    data['hour'] = data['pub_date'].dt.hour
    data['day_of_week'] = data['pub_date'].dt.day_name()

    # Distribusi laporan per jam
    st.write("Distribusi Laporan per Jam:")
    hourly_reports = data['hour'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    hourly_reports.plot(kind='bar', color='teal', ax=ax)
    ax.set_title('Distribusi Laporan per Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah')
    st.pyplot(fig)

    # Distribusi laporan per hari
    st.write("Distribusi Laporan per Hari:")
    daily_reports = data['day_of_week'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    daily_reports.plot(kind='bar', color='salmon', ax=ax)
    ax.set_title('Distribusi Laporan per Hari')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Jumlah')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

