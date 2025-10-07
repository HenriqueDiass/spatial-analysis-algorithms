# src/ui/components/sidra_section.py

import streamlit as st
import pandas as pd
import re
from typing import Optional, Dict, Any, List


from src.services.api_services import (
     buscar_lista_de_tabelas, 
     buscar_metadados_da_tabela, 
     buscar_dados_sidra
)

def display_tabela_selection_section() -> Optional[Dict[str, Any]]:
    """ SEÇÃO 1: Seleção da Tabela. Retorna os metadados da tabela selecionada. """
    st.header("1. Selecione a Tabela")
    
    lista_tabelas_formatada = buscar_lista_de_tabelas()
    metadados = None

    if lista_tabelas_formatada:
        opcoes_tabela = [f"{t['id']} - {t['nome']}" for t in lista_tabelas_formatada]
        
        tabela_selecionada_str = st.selectbox(
            label="Escolha uma tabela para inspecionar e consultar",
            options=opcoes_tabela,
            index=None,
            placeholder="Digite o código ou nome da tabela para pesquisar..."
        )

        if tabela_selecionada_str:
            id_selecionado = tabela_selecionada_str.split(" - ")[0]
            with st.spinner(f"Buscando metadados da tabela {id_selecionado}..."):
                metadados = buscar_metadados_da_tabela(int(id_selecionado))
                
        return metadados
    else:
        st.warning("Não foi possível carregar a lista de tabelas da API. Verifique se o backend está rodando corretamente.")
        return None


def display_sidra_query_section(metadados: Optional[Dict[str, Any]]):
    """ SEÇÃO 2: Consulta de Dados. """
    st.divider()
    st.header("2. Consultar Dados Gerais do SIDRA")

    if metadados is None:
        st.info("Selecione uma tabela na seção 1 para habilitar o formulário de consulta de dados.")
        return

    st.info(f"Parâmetros de consulta para a tabela: **{metadados.get('tabela_nome')}**")

    opcoes_niveis = {item['nome']: item['id'].replace('N', '') for item in metadados.get('niveis_territoriais', [])}
    opcoes_variaveis = {item['nome']: item['id'] for item in metadados.get('variaveis', [])}

    # Lógica do período
    opcoes_periodo = ["last", "all"]
    periodo_disponivel = metadados.get('periodo', {}).get('disponibilidade')
    if isinstance(periodo_disponivel, list):
        opcoes_periodo.extend(sorted(periodo_disponivel, reverse=True))
    elif isinstance(periodo_disponivel, str):
        anos_encontrados = re.findall(r'\b\d{4}\b', periodo_disponivel)
        if anos_encontrados:
            opcoes_periodo.extend(sorted(list(set(anos_encontrados)), reverse=True))

    with st.form("query_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Código da Tabela", value=metadados.get('tabela_id'), disabled=True)
            nivel_selecionado_label = st.selectbox("Nível Territorial*", options=list(opcoes_niveis.keys()), key="nivel_geral")
            ibge_code_input = st.text_input("Código Territorial", value="all", help="Use 'all' ou um código de UF (ex: 26 para PE)", key="ibge_geral")

        with col2:
            variaveis_selecionadas_labels = st.multiselect("Variável(eis) (opcional)", options=list(opcoes_variaveis.keys()), key="var_geral")
            period_input = st.selectbox("Período*", options=opcoes_periodo, key="periodo_geral")
        
        submitted = st.form_submit_button("Buscar Dados")

    if submitted:
        territorial_level_code = opcoes_niveis[nivel_selecionado_label]
        variable_codes = [opcoes_variaveis[label] for label in variaveis_selecionadas_labels]
        variable_param = ",".join(variable_codes) if variable_codes else None

        params = {
            "table_code": metadados.get('tabela_id'),
            "territorial_level": territorial_level_code,
            "ibge_territorial_code": ibge_code_input,
            "variable": variable_param,
            "period": period_input,
        }
        
        params = {k: v for k, v in params.items() if v}

        with st.spinner("Consultando a API do Sidra..."):
            dados = buscar_dados_sidra(params)
            if dados:
                st.success(f"{len(dados)} registros encontrados!")
                st.dataframe(pd.DataFrame(dados))