import streamlit as st
import pandas as pd
from typing import Dict, Any

from src.services.api_services import fetch_sim_data, fetch_sim_variables 

def display_sim_query_section():
    
    variables_data = fetch_sim_variables() 

    if not variables_data:
        st.error("Could not load SIM variables from the API. Check the systems list.")
        return

    st.header("System SIM")
    st.subheader(variables_data.get('description', 'Data Query'))

    variables_df = pd.DataFrame(variables_data['variables'])
    variables_df.columns = ["Code", "Group Name"] 
    
    group_code_dict = dict(zip(variables_df['Group Name'], variables_df['Code']))

    with st.expander("Available Variables (Groups)"):
        st.dataframe(variables_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.header("Query SIM Data by Group and State")
    
    with st.form("sim_query_form"):
        col_form_1, col_form_2, col_form_3 = st.columns(3)
        
        with col_form_1:
            selected_group_label = st.selectbox(
                "Select Group",
                options=list(group_code_dict.keys()),
                key="sim_group" 
            )
            
            selected_group_code = group_code_dict[selected_group_label]
            st.text_input("Group Code", value=selected_group_code, disabled=True)
            
        with col_form_2:
            single_year = st.number_input(
                "Year",
                min_value=1996, 
                max_value=2024,
                value=2022, 
                step=1,
                key="sim_year"
            )
            
        with col_form_3:
            single_state = st.text_input(
                "State (UF)",
                value="PE",
                max_chars=2,
                help="Enter one UF, or leave empty for all."
            ).upper()
            
        submitted = st.form_submit_button("Fetch SIM Data Summary")
    
    if submitted:
        year_list = [single_year] 
        state_list = [single_state] if single_state else None
        
        params: Dict[str, Any] = {
            "group_code": selected_group_code,
            "years": year_list,
            "states": state_list
        }
        
        st.info(f"Query parameters for API: Group={selected_group_code}, Years={year_list}, States={state_list}")

        with st.spinner("Fetching SIM data... This may take a moment."):
            
            data = fetch_sim_data(**params) 
            
            data_to_display = data.get('summary_by_municipality') if isinstance(data, dict) else None
            metadata = data.get('metadata', {}) if isinstance(data, dict) else {}
            
            columns_list = data.get('columns', data.get('available_columns', [])) 
            
            total_records = metadata.get('total_records_found', 0)
            
            if data_to_display and isinstance(data_to_display, list) and data_to_display:
                
                if total_records == 0:
                    total_records = len(data_to_display)
                
                st.success(f"✅ {total_records} records found for {selected_group_label}!")
                st.dataframe(pd.DataFrame(data_to_display), use_container_width=True)
                
                if columns_list: 
                    with st.expander(f"Show {len(columns_list)} available data columns for this group"):
                        columns_df = pd.DataFrame(columns_list, columns=["Column Name"])
                        st.dataframe(columns_df, use_container_width=True, hide_index=True)
                
            elif isinstance(data, dict) and data.get('summary_by_municipality') is not None:
                st.info(f"ℹ️ No records found for {selected_group_label} in {single_state} ({single_year}). Try different parameters.")
            else:
                st.error("Data fetching failed. Check the server console or API logs.")