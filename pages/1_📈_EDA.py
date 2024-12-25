import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fungsi import persiapan

# Konfigurasi halaman
st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📈")

# Memuat data
df_cuaca = persiapan('data')

# Header halaman
st.title("Analisis Data Cuaca")
st.markdown("Halaman ini digunakan untuk melakukan analisis eksplorasi data cuaca yang telah diproses.")

# Menampilkan data
st.subheader("Data Cuaca")
st.write(df_cuaca)

# Deskripsi statistik
st.subheader("Deskripsi Statistik")
st.write(df_cuaca.describe())

# Plot distribusi suhu
st.subheader("Distribusi Suhu")
fig, ax = plt.subplots()
sns.histplot(df_cuaca['suhu_rata2'], bins=20, kde=True, ax=ax)
ax.set_title("Distribusi Suhu Rata-rata")
ax.set_xlabel("Suhu Rata-rata (°C)")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Plot hubungan suhu dan curah hujan
st.subheader("Hubungan Suhu Rata-rata dan Curah Hujan")
fig, ax = plt.subplots()
sns.scatterplot(data=df_cuaca, x='suhu_rata2', y='curah_hujan', ax=ax)
ax.set_title("Suhu Rata-rata vs Curah Hujan")
ax.set_xlabel("Suhu Rata-rata (°C)")
ax.set_ylabel("Curah Hujan (mm)")
st.pyplot(fig)

# Filter data berdasarkan provinsi
st.subheader("Filter Data Berdasarkan Provinsi")
provinsi = st.selectbox("Pilih Provinsi", df_cuaca['province_name'].unique())
filtered_data = df_cuaca[df_cuaca['province_name'] == provinsi]
st.write(filtered_data)

# Visualisasi suhu rata-rata per provinsi
st.subheader("Suhu Rata-rata per Provinsi")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_cuaca, x='province_name', y='suhu_rata2', ax=ax)
ax.set_title("Suhu Rata-rata per Provinsi")
ax.set_xlabel("Provinsi")
ax.set_ylabel("Suhu Rata-rata (°C)")
ax.tick_params(axis='x', rotation=90)
st.pyplot(fig)

# Menambahkan insight tambahan
st.subheader("Insight Tambahan")
st.markdown("""
- Data menunjukkan distribusi suhu rata-rata cukup simetris pada sebagian besar provinsi.
- Curah hujan memiliki hubungan yang tidak linear dengan suhu rata-rata.
- Filter data memungkinkan analisis per provinsi untuk memahami karakteristik lokal.
""")
