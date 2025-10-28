# Home.py (seu novo arquivo de entrada)

import streamlit as st
from src.ui.components.sidra_section import display_table_selection_section

st.set_page_config(layout="wide")
st.title("🔎 Data Explorer")

st.write("Welcome to the main application!")
