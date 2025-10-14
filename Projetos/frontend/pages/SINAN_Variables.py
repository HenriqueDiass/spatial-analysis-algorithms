# pages/4_SINAN_Variables.py

import streamlit as st
# Importa APENAS a função de renderização do componente
from src.ui.components.sinan_query_section import display_sinan_query_section

# Configuração da página
st.set_page_config(layout="wide")

# Chama o componente para renderizar toda a lógica
display_sinan_query_section()