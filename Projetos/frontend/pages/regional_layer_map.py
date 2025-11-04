import streamlit as st
from src.ui.components.regional_layer_map_section import display_regional_layers_section

st.set_page_config(layout="wide")
st.title("📚 Regional layer")
st.markdown("---")
display_regional_layers_section()