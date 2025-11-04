import streamlit as st
from io import BytesIO
from src.services.api_services import fetch_regional_layers_map


def display_regional_layers_section():
    
    st.header("Mapa de Camadas Regionais")
    st.markdown("Gere um mapa exibindo as divisões geográficas de um estado.")

    YEAR = 2020

    with st.form("regional_map_form"):
        
        
        state_abbr = st.text_input(
            "Sigla do Estado (UF)",
            value="PE",
            max_chars=2,
            help="Ex: PE, SP, BA."
        ).upper()
        
        st.markdown("---")
        st.subheader("Opções de Camadas e Visualização")
        
        
        col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4)
        
        with col_opt1:
            show_mun = st.checkbox("Municípios", value=False)
        
        with col_opt2:
            show_imm = st.checkbox("Reg. Imediatas", value=False)
            
        with col_opt3:
            show_int = st.checkbox("Reg. Intermediárias", value=False)
            
        with col_opt4:
            use_zoom = st.checkbox("Aplicar Zoom", value=False, help="Foca o mapa no estado, em vez de mostrar o Brasil.")
            
        
        
        map_submitted = st.form_submit_button("Gerar Mapa Regional")

    
    if map_submitted:
        if not state_abbr or len(state_abbr) != 2:
            st.warning("Por favor, insira uma sigla de UF válida com 2 caracteres.")
            return 

        
        layers = []
        if show_mun: layers.append("Municípios")
        if show_imm: layers.append("Imediatas")
        if show_int: layers.append("Intermediárias")
        
        
        if not layers:
            caption_text = f"Mapa de contorno para {state_abbr} ({YEAR})"
        else:
            caption_text = f"Camadas ({', '.join(layers)}) para {state_abbr} ({YEAR})"

        # Chama a API
        with st.spinner(f"Gerando mapa de camadas para {state_abbr} ({YEAR})..."):
            map_content = fetch_regional_layers_map(
                state_abbr=state_abbr,
                year=YEAR, 
                show_municipalities=show_mun,
                show_immediate=show_imm,
                show_intermediate=show_int,
                use_zoom=use_zoom
            )

            if map_content:
                st.success("✅ Mapa gerado com sucesso!")
                st.image(
                    BytesIO(map_content),
                    caption=caption_text,
                    use_container_width=True,
                    width=700
                    
                )
            else:
                st.warning("Falha ao gerar o mapa. Verifique os detalhes do erro acima.")