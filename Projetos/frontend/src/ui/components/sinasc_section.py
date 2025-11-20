import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from io import BytesIO

# Imports dos serviços
from src.services.api_services import (
    fetch_sinasc_variables,
    fetch_sinasc_data,
    fetch_birthrate_map
)

from src.ui.constants import METRIC_OPTIONS

def display_sinasc_query_section():
    
    # ==============================================================================
    # 1. CARREGAMENTO INICIAL E CABEÇALHO
    # ==============================================================================
    variables_data = fetch_sinasc_variables()

    if not variables_data:
        st.error("Could not load SINASC variables. Check API.")
        return

    st.header("System SINASC")
    st.subheader(variables_data.get('description', 'Data Query'))

    # Processamento das variáveis para o Selectbox
    raw_vars = variables_data.get('variables', variables_data)
    group_codes = {}

    if isinstance(raw_vars, list):
        variables_df = pd.DataFrame(raw_vars)
        if variables_df.shape[1] >= 2:
            variables_df.columns = ["Code", "Group/Variable Name"]
            group_codes = dict(zip(variables_df['Group/Variable Name'], variables_df['Code']))
        else:
            st.error("Unexpected variable format.")
            return
    else:
        st.error("Data format not recognized.")
        return

    with st.expander("Available Variables (Groups)"):
        st.dataframe(variables_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    
    st.header("Parâmetros de Análise ")
    
    with st.container():
        col_global_1, col_global_2, col_global_3 = st.columns(3)
        
        with col_global_1:
            selected_group_label = st.selectbox(
                "Select Group/Variable",
                options=list(group_codes.keys()),
                key="sinasc_global_group"
            )
            group_code = group_codes[selected_group_label]
            st.text_input("Group Code", value=group_code, disabled=True)
            
        with col_global_2:
            global_year = st.number_input(
                "Year",
                min_value=2000, max_value=2024, value=2022, 
                step=1, key="sinasc_global_year"
            )
            
        with col_global_3:
            global_state = st.text_input(
                "State (UF)",
                value="PE", max_chars=2,
                help="Leave empty for all (Table only).",
                key="sinasc_global_state"
            ).upper()

    st.markdown("---")

    tab_data, tab_map = st.tabs(["📊 Dados Detalhados (Tabela)", "🗺️ Mapa de Natalidade"])

    with tab_data:
        st.subheader(f"Tabela: {selected_group_label}")
        
        if st.button("Carregar Tabela de Dados", key="btn_load_table"):
            year_list = [global_year] 
            state_list = [global_state] if global_state else None
            
            st.info(f"Buscando dados: {group_code}, Ano: {global_year}, Estado: {global_state}")

            with st.spinner("Fetching SINASC data..."):
                data = fetch_sinasc_data(
                    group_code=group_code,
                    years=year_list,
                    states=state_list
                )
                
                summary_dict = data.get('summary', {}) if data else {}
                columns_list = data.get('columns', []) if data else []
                
                rows_to_display = []

                if summary_dict:
                    for mun_code, stats in summary_dict.items():
                        
                        row = {
                            "Município Code": mun_code.strip(),
                            "Total Nascimentos": stats.get('total', 0)
                        }
                        
                        if 'by_sex' in stats:
                            row['Masc (1)'] = stats['by_sex'].get('1', 0)
                            row['Fem (2)'] = stats['by_sex'].get('2', 0)
                            
                        if 'by_mother_age_group' in stats:
                            for age_group, count in stats['by_mother_age_group'].items():
                                row[f"Mãe {age_group}"] = count

                        rows_to_display.append(row)

                if rows_to_display:
                    total_records = len(rows_to_display)
                    st.success(f"✅ Encontrados dados para {total_records} municípios!")
                    
                    st.dataframe(pd.DataFrame(rows_to_display), use_container_width=True)
                    
                    if columns_list: 
                        with st.expander(f"Show raw columns"):
                            st.write(columns_list)
                
                elif not summary_dict and data:
                     st.warning("Data received but 'summary' dictionary is empty.")
                else:
                    st.info(f"ℹ️ No records found. Try different parameters.")

    with tab_map:
        st.subheader("Visualização Espacial")
        
        col_metric, col_btn = st.columns([3, 1])
        
        with col_metric:
            metric_label_map = st.selectbox(
                "Metric to Map",
                options=list(METRIC_OPTIONS.keys()),
                key="sinasc_map_metric"
            )
        
        with col_btn:
            st.write("") 
            st.write("")
            generate_map = st.button("Gerar Mapa", key="btn_gen_map")

        if generate_map:
            # Validação: Mapa precisa de UF
            if not global_state or len(global_state) != 2:
                st.warning("⚠️ Para gerar o mapa, preencha o campo 'State (UF)' nos filtros acima.")
            else:
                metric_column_name = METRIC_OPTIONS[metric_label_map]

                with st.spinner(f"Generating map for {global_state} ({global_year})..."):
                    
                    map_content = fetch_birthrate_map(
                        state_abbr=global_state, 
                        year=global_year,         
                        metric_column=metric_column_name
                    )

                    if map_content:
                        st.success("✅ Map generated successfully!")
                        st.image(
                            BytesIO(map_content),
                            caption=f"Map: {metric_label_map} in {global_state}/{global_year}",
                            use_container_width=True
                        )
                    else:
                        st.error("Failed to generate map. Check API logs.")