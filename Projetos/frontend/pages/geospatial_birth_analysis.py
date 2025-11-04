#Geographical_Maps.py


import streamlit as st
from src.ui.components.maps_section import display_map_generation_section

st.set_page_config(layout="wide")

st.title("🗺️ Geographical Map Generator")
st.markdown("---")

display_map_generation_section()