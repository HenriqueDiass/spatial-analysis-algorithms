# src/ui/components/sinan_query_section.py

import streamlit as st
import pandas as pd
from typing import Dict, Any, List

from src.services.api_services import (
    fetch_sinan_variables,
    fetch_sinan_data
)

def display_sinan_query_section():
    
    variables_data = fetch_sinan_variables()

    if not variables_data:
        st.error("Could not load SINAN variables from the API. Check the systems list.")
        return

    st.header(f"System: {variables_data.get('informationSystem', 'SINAN')}")
    st.subheader(variables_data.get('description', 'Data Query'))

    variables_df = pd.DataFrame(variables_data['variables'])
    variables_df.columns = ["Code", "Disease/Condition Name"]
    disease_codes = dict(zip(variables_df['Disease/Condition Name'], variables_df['Code']))

    with st.expander("Available Variables (Diseases)"):
        st.dataframe(variables_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.header("Query SINAN Data by Disease and State (Limited to 1 Year/State)")
    
    with st.form("sinan_query_form"):
        col_form_1, col_form_2, col_form_3 = st.columns(3)
        
        with col_form_1:
            selected_disease_label = st.selectbox(
                "Select Disease/Condition",
                options=list(disease_codes.keys()),
                key="sinan_disease"
            )
            disease_code = disease_codes[selected_disease_label]
            st.text_input("Disease Code", value=disease_code, disabled=True)
            
        with col_form_2:
            single_year = st.number_input(
                "Year",
                min_value=2000,
                max_value=2024,
                value=2022, 
                step=1,
                key="sinan_year"
            )
            
        with col_form_3:
            single_state = st.text_input(
                "State (UF)",
                value="PE",
                max_chars=2,
                help="Enter one UF, or leave empty for all."
            ).upper()
            
        submitted = st.form_submit_button("Fetch SINAN Data Summary")
    
    if submitted:
        year_list = [single_year] 
        state_list = [single_state] if single_state else None
        
        params: Dict[str, Any] = {
             "disease_code": disease_code,
             "years": year_list,
             "states": state_list
        }
        
        st.info(f"Query parameters for API: Disease={disease_code}, Years={year_list}, States={state_list}")

        with st.spinner("Fetching SINAN data... This may take a moment."):
            data = fetch_sinan_data(params) 
            
            data_to_display = data.get('summary_by_municipality') if isinstance(data, dict) else None
            total_records = data.get('metadata', {}).get('total_records_found', 0) if isinstance(data, dict) else 0

            if data_to_display and isinstance(data_to_display, list) and data_to_display:
                
                st.success(f"✅ {total_records} records found for {selected_disease_label}!")
                st.dataframe(pd.DataFrame(data_to_display), use_container_width=True)
            elif total_records == 0:
                st.info(f"ℹ️ No records found for {selected_disease_label} in {single_state} ({single_year}). Try different parameters.")
            else:
                st.error("Data fetching failed. Check the server console for 500 errors or malformed response.")