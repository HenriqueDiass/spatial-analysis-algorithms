
import streamlit as st
from src.ui.components.sim_section import display_sim_query_section


st.set_page_config(layout="wide")

# Chama o componente para renderizar toda a lógica
display_sim_query_section()