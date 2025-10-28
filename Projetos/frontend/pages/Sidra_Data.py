# pages/Sidra_Data.py

import streamlit as st

from src.ui.components.sidra_section import (
    display_table_selection_section,
    display_sidra_query_section
)
st.set_page_config(layout="wide")
st.title("📊 SIDRA Data Query")
st.markdown("---")

metadata = display_table_selection_section()
display_sidra_query_section(metadata)
