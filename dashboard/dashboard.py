import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul dashboard
st.title('Air Quality Analysis Dashboard: Stasiun Gucheng')

# Deskripsi
st.write('Dashboard ini memberikan pengalaman interaktif dalam mengeksplorasi data kualitas udara, dengan fokus utama pada tingkat PM10 serta keterkaitannya dengan berbagai faktor cuaca.')

# About me
st.markdown("""
### About Me
- **Name**: Silvia Febriani
- **Email Address**: silviafebriani608@gmail.com
- **Dicoding ID**: silviafebr

### Project Overview
Dashboard ini menyajikan analisis data kualitas udara dengan fokus pada tingkat PM10 di stasiun Gucheng. Proyek ini bertujuan untuk mengidentifikasi pola, variasi musiman, serta pengaruh berbagai kondisi cuaca terhadap kualitas udara. Wawasan yang diperoleh dari analisis ini diharapkan dapat mendukung studi lingkungan dan pemantauan kesehatan masyarakat.
""")

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("main_data.csv")
    
    # Cek apakah kolom 'tahun' ada
    if 'tahun' not in data.columns:
        st.error("Kolom 'tahun' tidak ditemukan di dataset! Cek kembali file CSV.")
        st.stop()  # Hentikan eksekusi jika kolom 'tahun' tidak ada
    
    return data

data = load_data()

# Menambahkan sidebar untuk input interaktif
st.sidebar.header('Fitur Input User')

# Memungkinkan users memilih tahun dan bulan untuk melihat data
selected_year = st.sidebar.selectbox('Pilih Tahun', list(data['tahun'].unique()))
selected_month = st.sidebar.selectbox('Pilih Bulan', list(data['bulan'].unique()))

# Filter data berdasarkan tahun dan bulan yang dipilih
data_filtered = data[(data['tahun'] == selected_year) & (data['bulan'] == selected_month)].copy()

# Menampilkan statistik data
st.subheader('Tinjauan Data untuk Periode yang Dipilih')
st.write(data_filtered.describe())

# Line chart untuk tingkat PM10 selama bulan yang dipilih
st.subheader('Tingkat PM10 Harian')
fig, ax = plt.subplots()
ax.plot(data_filtered['hari'], data_filtered['PM10'])
plt.xlabel('Hari dalam Sebulan')
plt.ylabel('Konsentrasi PM10')
st.pyplot(fig)

# Analisis Pola Musiman
st.subheader('Analisis Pola Musiman')
seasonal_trends = data.groupby('bulan')['PM10'].mean()
fig, ax = plt.subplots()
seasonal_trends.plot(kind='bar', color='pink', ax=ax)
plt.title('Rata-rata Tingkat PM10 Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata PM10')
st.pyplot(fig)

# Rata-rata Heatmap per jam
st.subheader('Rata-rata PM10 per jam')
try:
    # Memastikan tipe data yang benar dan menangani nilai yang hilang
    data['jam'] = data['jam'].astype(int)
    data['PM10'] = pd.to_numeric(data['PM10'], errors='coerce')
    data['PM10'].ffill(inplace=True)

    # Menghitung rata-rata per jam
    hourly_avg = data.groupby('jam')['PM10'].mean()

    # Plotting
    fig, ax = plt.subplots()
    sns.heatmap([hourly_avg.values], ax=ax, cmap='coolwarm')
    plt.title('Rata-rata PM10 per jam')
    st.pyplot(fig)
except Exception as e:
    st.error(f"Error dalam memplotkan rata-rata per jam: {e}")

# Membandingkan Curah Hujan dengan Kualitas Udara
st.subheader('Membandingkan Curah Hujan dengan tingkat PM10')
fig, ax = plt.subplots()
sns.scatterplot(x='HUJAN', y='PM10', data=data_filtered, ax=ax)
plt.title('Perbandingan Curah Hujan dengan tingkat PM10')
st.pyplot(fig)

# Korelasi Heatmap - Interaktif
st.subheader('Korelasi Heatmap Interaktif')
selected_columns = st.multiselect('Pilih Kolom untuk Korelasi', data.columns, default=['PM10', 'NO2', 'TEMP', 'PRES', 'DEWP'])
corr = data[selected_columns].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)


# Kesimpulan
st.subheader('Kesimpulan')
st.write("""
Dashboard ini menyajikan analisis mendalam mengenai kualitas udara dengan fokus utama pada tingkat PM10. Melalui berbagai visualisasi interaktif, pengguna dapat memahami distribusi PM10 serta faktor-faktor yang memengaruhinya. 

Pola musiman dan dampak kondisi cuaca terhadap kualitas udara ditampilkan secara jelas, memberikan wawasan mengenai tren yang terjadi sepanjang tahun. Selain itu, dashboard ini memungkinkan eksplorasi data secara fleksibel, sehingga pengguna dapat memperoleh pemahaman yang lebih dalam mengenai hubungan antara kualitas udara dan berbagai variabel lingkungan.
""")
