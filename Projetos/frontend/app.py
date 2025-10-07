# app.py

import streamlit as st

from src.ui.components.sidra_section import (
    display_tabela_selection_section, 
    display_sidra_query_section
)
from src.ui.components.maps_section import display_map_generation_section


# Configuração básica
st.set_page_config(layout="wide")
st.title("🔎 Explorador de Dados e Mapas Geográficos")

def main():
    metadados = display_tabela_selection_section()
    
    display_sidra_query_section(metadados)
    
    display_map_generation_section()

if __name__ == "__main__":
    main()