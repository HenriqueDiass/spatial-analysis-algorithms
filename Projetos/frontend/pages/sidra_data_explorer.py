import streamlit as st
# Importe a NOVA função principal do arquivo que criamos
from src.ui.components.sidra_section import display_sidra_query_component

st.set_page_config(layout="wide")
st.title("📊 SIDRA Data Query")
st.markdown("---")

# Chame a função única que faz todo o trabalho
display_sidra_query_component()