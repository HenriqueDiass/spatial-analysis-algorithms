#Geographical_Maps.py


import streamlit as st
from src.ui.components.sidra_section import display_table_selection_section 

st.set_page_config(layout="wide")

st.title("🗺️ Geographical Map Generator")
st.markdown("---")

display_table_selection_section()