# src/ui/components/maps_section.py

import streamlit as st
from io import BytesIO
from src.services.api_services import buscar_mapa_de_natalidade

from src.ui.constants import METRIC_OPTIONS

def display_map_generation_section():
    """ SEÇÃO 3: Geração de Mapas. """
    st.divider()
    st.header("3. Gerar Mapa de Natalidade por Estado")

    with st.container():
        col_mapa_1, col_mapa_2 = st.columns(2)
        
        with col_mapa_1:
            state_abbr_mapa = st.text_input(
                "Sigla do Estado (UF)", 
                value="PE", 
                max_chars=2, 
                help="Ex: PE, SP, BA."
            ).upper()
        
        with col_mapa_2:
            year_mapa = st.number_input(
                "Ano da Análise (SINASC/População)", 
                min_value=2010, 
                max_value=2024, 
                value=2022, 
                step=1
            )

        metric_label_mapa = st.selectbox(
            "Métrica para Mapear", 
            options=list(METRIC_OPTIONS.keys())
        )
        
        map_submitted = st.button("Gerar Mapa Coroplético")

    if map_submitted and state_abbr_mapa and len(state_abbr_mapa) == 2:
        metric_column_name = METRIC_OPTIONS[metric_label_mapa]
        
        with st.spinner(f"Gerando mapa coroplético de {metric_label_mapa} para {state_abbr_mapa} no ano {year_mapa}..."):
            map_content = buscar_mapa_de_natalidade(
                state_abbr=state_abbr_mapa,
                year=year_mapa,
                metric_column=metric_column_name
            )

            if map_content:
                st.success("✅ Mapa gerado com sucesso!")
                st.image(
                    BytesIO(map_content), 
                    caption=f"Mapa: {metric_label_mapa} em {state_abbr_mapa}/{year_mapa}", 
                    use_container_width=True
                )