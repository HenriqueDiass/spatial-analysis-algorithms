import streamlit as st
import pandas as pd
from typing import Dict, Any

# --- CORREÇÃO 1: Importar as DUAS funções ---
# fetch_sim_variables -> Busca a lista de grupos (ex: CID10)
# fetch_sim_data -> Busca os dados de mortalidade
from src.services.api_services import fetch_sim_data, fetch_sim_variables 

def display_sim_query_section():
    
    # --- CORREÇÃO 2: Chamar a função correta para buscar variáveis ---
    # Você estava chamando fetch_sim_data() aqui por engano.
    variables_data = fetch_sim_variables() 

    if not variables_data:
        st.error("Could not load SIM variables from the API. Check the systems list.")
        return

    st.header("System SIM")
    st.subheader(variables_data.get('description', 'Data Query'))

    # Assumindo que a API de variáveis retorna uma chave 'variables'
    variables_df = pd.DataFrame(variables_data['variables'])
    # Renomeando colunas para clareza
    variables_df.columns = ["Code", "Group Name"] 
    
    # --- CORREÇÃO 3: Renomear variável para evitar conflito ---
    # 'group_code' -> 'group_code_dict'
    group_code_dict = dict(zip(variables_df['Group Name'], variables_df['Code']))

    with st.expander("Available Variables (Groups)"):
        st.dataframe(variables_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.header("Query SIM Data by Group and State")
    
    with st.form("sim_query_form"):
        col_form_1, col_form_2, col_form_3 = st.columns(3)
        
        with col_form_1:
            selected_group_label = st.selectbox(
                "Select Group", # Label atualizado
                options=list(group_code_dict.keys()),
                key="sim_group" # Key atualizada
            )
            # --- CORREÇÃO 3: Usar as variáveis com nomes claros ---
            selected_group_code = group_code_dict[selected_group_label]
            st.text_input("Group Code", value=selected_group_code, disabled=True)
            
        with col_form_2:
            single_year = st.number_input(
                "Year",
                min_value=1996, # SIM tem dados mais antigos
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
        
        # Monta o dicionário de parâmetros
        params: Dict[str, Any] = {
            "group_code": selected_group_code, # --- CORREÇÃO 3 ---
            "years": year_list,
            "states": state_list
        }
        
        st.info(f"Query parameters for API: Group={selected_group_code}, Years={year_list}, States={state_list}")

        # --- CORREÇÃO 4: Atualizar texto do spinner ---
        with st.spinner("Fetching SIM data... This may take a moment."):
            
            # --- CORREÇÃO 5: Usar o operador (**) para desempacotar o dicionário ---
            # A função fetch_sim_data(group_code=..., years=..., states=...)
            # precisa dos argumentos nomeados, não de um dicionário.
            data = fetch_sim_data(**params) 
            
            data_to_display = data.get('summary_by_municipality') if isinstance(data, dict) else None
            metadata = data.get('metadata', {}) if isinstance(data, dict) else {}
            
            
            total_records = metadata.get('total_records_found', 0)
            # A API do SIM pode não retornar 'columns', então ajustamos
            columns_list = metadata.get('available_columns', []) 

            if data_to_display and isinstance(data_to_display, list) and data_to_display:
                
                # Se total_records não veio, usa o len do dataframe
                if total_records == 0:
                    total_records = len(data_to_display)
                
                st.success(f"✅ {total_records} records found for {selected_group_label}!")
                st.dataframe(pd.DataFrame(data_to_display), use_container_width=True)
                
                if columns_list: 
                    with st.expander(f"Show {len(columns_list)} available data columns for this group"):
                        columns_df = pd.DataFrame(columns_list, columns=["Column Name"])
                        st.dataframe(columns_df, use_container_width=True, hide_index=True)
                
            elif isinstance(data, dict) and data.get('summary_by_municipality') is not None:
                # A API respondeu, mas o sumário está vazio
                st.info(f"ℹ️ No records found for {selected_group_label} in {single_state} ({single_year}). Try different parameters.")
            else:
                # 'data' pode ser None se a API falhou
                st.error("Data fetching failed. Check the server console or API logs.")