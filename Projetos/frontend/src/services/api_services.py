# src/services/api_service.py

import streamlit as st
import requests
from typing import Optional, Dict, Any, List
from src.ui.constants import API_URL

@st.cache_data
def buscar_lista_de_tabelas() -> Optional[List[Dict[str, Any]]]:
    # Lógica de buscar_lista_de_tabelas (mantida, usando API_URL do constants)
    try:
        response = requests.get(f"{API_URL}/sidra/tables")
        response.raise_for_status()
        # ... (Restante da lógica)
        dados_brutos = response.json()
        
        lista_final_de_tabelas = []
        for pesquisa in dados_brutos:
            if "agregados" in pesquisa and isinstance(pesquisa["agregados"], list):
                for tabela in pesquisa["agregados"]:
                    lista_final_de_tabelas.append({
                        "id": tabela["id"],
                        "nome": tabela["nome"]
                    })
        
        return sorted(lista_final_de_tabelas, key=lambda x: int(x['id']))
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com a API para buscar tabelas: {e}")
        return None

@st.cache_data
def buscar_metadados_da_tabela(table_id: int) -> Optional[Dict[str, Any]]:
    # Lógica de buscar_metadados_da_tabela (mantida)
    try:
        response = requests.get(f"{API_URL}/sidra/tables/{table_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def buscar_dados_sidra(params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """ Nova função para buscar dados de consulta da Seção 2. """
    try:
        response = requests.get(f"{API_URL}/sidra/tables/fetch-specific", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Erro ao buscar os dados na API.")
        if e.response is not None:
            try:
                st.json(e.response.json())
            except:
                st.write(f"Detalhes do erro: {e}")
        return None

def buscar_mapa_de_natalidade(state_abbr: str, year: int, metric_column: str) -> Optional[bytes]:
    # Lógica de buscar_mapa_de_natalidade (mantida, usando API_URL do constants)
    base_url = f"{API_URL}/maps/{state_abbr}/{year}/birth-rate"
    
    params = {
        "metric": metric_column,
        "group_code": "DN" 
    }
    
    st.info(f"Chamando API: {base_url} com métrica: {metric_column}")
    
    try:
        response = requests.get(base_url, params=params, timeout=60) 
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao gerar o mapa na API.")
        if e.response is not None:
             try:
                 error_detail = e.response.json().get("detail", e.response.text)
                 st.write(f"Detalhes do erro do servidor: {error_detail}")
             except:
                 st.write(f"Detalhes do erro de rede: {e}")
        return None