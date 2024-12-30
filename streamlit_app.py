import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="Beranda",
    page_icon="🏠",
)

st.title("Dashboard Cuaca")
st.subheader("Mindstem.id")

st.markdown(
    """Dashboard Machine Learning untuk Data Cuaca Indonesia. 
            Sumber data: https://www.kaggle.com/datasets/greegtitan/indonesia-climate,
            diolah dari data BMKG tahun 2010-2020""")


fig = go.Figure(data=go.Choropleth(
    geojson="https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson",
    featureidkey="properties.kode",
    locations=["ID"],
    marker_line_color='darkgray',
    marker_line_width=0.5,
))

fig.update_layout(
    title_text='Peta Indonesia',
    geo_scope='asia',
    geo=dict(
        center=dict(lat=-2, lon=118),
        projection_scale=3,
        showland=True,
        landcolor="lightgreen",  # Warna daratan: hijau muda
        showocean=True,
        oceancolor="skyblue",  # Warna lautan: biru langit
        showcountries=True,
        countrycolor="black",
        coastlinecolor="black"
    )
)

st.plotly_chart(fig, use_container_width=True) 

st.sidebar.success("Pilih Opsi")

st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: gray;">
        &copy; 2024 Mindstem.id. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)