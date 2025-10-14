# pages/Sidra_Data.py

import streamlit as st
# Importa as funções do seu módulo (assumindo que o caminho está correto: src/ui/components)
from src.ui.components.sidra_section import (
    display_table_selection_section,
    display_sidra_query_section
)
st.set_page_config(layout="wide")
st.title("📊 SIDRA Data Query")
st.markdown("---")

# Renderiza as duas seções SIDRA em sequência
metadata = display_table_selection_section()
display_sidra_query_section(metadata)

# Este arquivo agora é acessível em sua_url/Sidra_Data