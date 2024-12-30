import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up the page configuration
st.set_page_config(
    page_title="Beranda",
    page_icon="🏠",
)

st.title("Dashboard Cuaca")
st.subheader("Mindstem.id")

st.markdown(
    """Dashboard Machine Learning untuk Data Cuaca Indonesia. 
       Sumber data: https://www.kaggle.com/datasets/greegtitan/indonesia-climate,
       diolah dari data BMKG tahun 2010-2020"""
)

# Load station data
try:
    station_data = pd.read_csv("data/station_detail.csv")
    st.success("Data berhasil dimuat!")
except FileNotFoundError:
    st.error("File 'station_detail.csv' tidak ditemukan. Pastikan file tersebut ada di folder 'data'.")
    st.stop()

# Prepare data for the map
latitudes = station_data["latitude"]
longitudes = station_data["longitude"]
station_names = station_data["station_name"]  # Assuming there's a station_name column

# Create the map with Plotly
fig = go.Figure()

# Add the base map (choropleth)
fig.add_trace(go.Choropleth(
    geojson="https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson",
    featureidkey="properties.kode",
    locations=["ID"],
    marker_line_color='darkgray',
    marker_line_width=0.5,
))

# Add station points
fig.add_trace(go.Scattergeo(
    lon=longitudes,
    lat=latitudes,
    text=station_names,
    mode="markers",
    marker=dict(
        size=8,
        color="red",
        symbol="circle"
    ),
    name="Weather Stations"
))

# Update layout
fig.update_layout(
    title_text='Peta Indonesia dengan Titik Stasiun Cuaca',
    geo_scope='asia',
    geo=dict(
        center=dict(lat=-2, lon=118),
        projection_scale=3,
        showland=True,
        landcolor="lightgreen",
        showocean=True,
        oceancolor="skyblue",
        showcountries=True,
        countrycolor="black",
        coastlinecolor="black"
    )
)

st.plotly_chart(fig, use_container_width=True)

# Sidebar options
st.sidebar.success("Pilih Opsi")

st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: gray;">
        &copy; 2024 Mindstem.id. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
