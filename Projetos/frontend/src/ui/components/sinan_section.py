import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from io import BytesIO
from src.services.api_services import fetch_prevalence_map

from src.ui.constants import METRIC_OPTIONS_SINAN

from src.services.api_services import (
    fetch_sinan_variables,
    fetch_sinan_data
)

def display_sinan_query_section():
    
    variables_data = fetch_sinan_variables()

    if not variables_data:
        st.error("Could not load SINAN variables from the API. Check the systems list.")
        return

    st.header("System SINAN")
    st.subheader(variables_data.get('description', 'Data Query'))

    variables_df = pd.DataFrame(variables_data['variables'])
    variables_df.columns = ["Code", "Disease/Condition Name"]
    disease_codes = dict(zip(variables_df['Disease/Condition Name'], variables_df['Code']))

    with st.expander("Available Variables (Diseases)"):
        st.dataframe(variables_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.header("Query SINAN Data by Disease and State")
    
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
            metadata = data.get('metadata', {}) if isinstance(data, dict) else {}
            
            
            total_records = metadata.get('total_records_found', 0)
            columns_list = metadata.get('columns', []) 

            if data_to_display and isinstance(data_to_display, list) and data_to_display:
                
                st.success(f"✅ {total_records} records found for {selected_disease_label}!")
                
                
                st.dataframe(pd.DataFrame(data_to_display), use_container_width=True)
                
                
                if columns_list: 
                    with st.expander(f"Show {len(columns_list)} available data columns for this disease"):
                        columns_df = pd.DataFrame(columns_list, columns=["Column Name"])
                        st.dataframe(columns_df, use_container_width=True, hide_index=True)
                
                    
            elif total_records == 0:
                st.info(f"ℹ️ No records found for {selected_disease_label} in {single_state} ({single_year}). Try different parameters.")
            else:
                st.error("Data fetching failed. Check the server console for 500 errors or malformed response.")


    st.header("Mapa de Prevalencia")
    with st.container():
        col_map_1, col_map_2 = st.columns(2)

        with col_map_1:
            state_abbr_map = st.text_input(
                "State Abbreviation (UF)",
                value="PE",
                max_chars=2,
                help="Ex: PE, SP, BA."
            ).upper()

        with col_map_2:
            year_map = st.number_input(
                "Analysis Year (SINASC/Population)",
                min_value=2010,
                max_value=2024,
                value=2022,
                step=1
            )

        variable_sinan = st.selectbox(
            "Select Disease/Condition",  
            options=list(disease_codes.keys())       
        )

        metric_label_map = st.selectbox(
            "Metric to Map",
            options=list(METRIC_OPTIONS_SINAN.keys())   
        )

        map_submitted = st.button("Generate Choropleth Map")

    if map_submitted and state_abbr_map and len(state_abbr_map) == 2:
        
        metric_column_name = METRIC_OPTIONS_SINAN[metric_label_map]
        
        
        disease_code_map = disease_codes[variable_sinan]

        
        with st.spinner(f"Generating choropleth map for {variable_sinan} ({metric_label_map}) in {state_abbr_map} for {year_map}..."):
            map_content = fetch_prevalence_map(
                state_abbr=state_abbr_map,
                year=year_map,
                metric=metric_column_name,
                disease_code=disease_code_map  
            )

            if map_content:
                st.success("✅ Map generated successfully!")
                st.image(
                    BytesIO(map_content),
                    caption=f"Map: {variable_sinan} ({metric_label_map}) in {state_abbr_map}/{year_map}",
                    use_container_width=True
                )
            
            else:
                st.error(f"Failed to generate map for {variable_sinan}. The API returned no content.")