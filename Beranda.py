import streamlit as st

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

st.sidebar.success("Pilih Opsi")

