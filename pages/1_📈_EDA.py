import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fungsi import persiapan, plot_time_series, plot_time_series_plotly

# Konfigurasi halaman
st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📈")

# Memuat data
if 'df_cuaca' not in st.session_state:
    df_cuaca = persiapan('data')
    st.session_state.df_cuaca = df_cuaca
df_cuaca = st.session_state.df_cuaca

# Header halaman
st.title("Analisis Data Cuaca")
st.markdown("Halaman ini digunakan untuk melakukan analisis eksplorasi data cuaca yang telah diproses.")

# Tambahkan opsi "Total Indonesia" ke daftar provinsi
daftar_provinsi = ['Total Indonesia'] + list(df_cuaca['province_name'].unique())

# Filter data berdasarkan provinsi
st.subheader("Filter Data Berdasarkan Provinsi")
provinsi = st.selectbox("Pilih Provinsi", daftar_provinsi)

# Tangani kasus "Total Indonesia"
if provinsi == 'Total Indonesia':
    df_cuaca_prov = df_cuaca.copy() # Membuat salinan agar tidak memodifikasi DataFrame asli
else:
    df_cuaca_prov = df_cuaca[df_cuaca['province_name'] == provinsi]


# Deskripsi statistik
st.subheader("Deskripsi Statistik")
st.write(df_cuaca_prov.describe())

# Daftar variabel yang tersedia untuk dipilih
pilihan_variabel = ["suhu", "kelembaban", "curah_hujan", "kecepatan_angin", "durasi_sinar_matahari_jam"]

# Membuat dropdown
variabel_terpilih = st.selectbox("Pilih Variabel:", pilihan_variabel)

# Membuat plot berdasarkan pilihan dropdown
if variabel_terpilih:  # Pastikan ada variabel yang dipilih
    try:
        fig = plot_time_series_plotly(df_cuaca_prov, variabel_terpilih)
        st.plotly_chart(fig)
    except ValueError as e:
        st.error(str(e)) # Menampilkan pesan error jika variabel tidak valid
