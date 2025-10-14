# src/services/api_service.py

import streamlit as st
import requests
from typing import Optional, Dict, Any, List
from src.ui.constants import API_URL

@st.cache_data
def fetch_table_list() -> Optional[List[Dict[str, Any]]]:
    """Fetches the list of all available tables from the API."""
    try:
        response = requests.get(f"{API_URL}/sidra/tables")
        response.raise_for_status()

        raw_data = response.json()

        final_table_list = []
        for research in raw_data:
            if "agregados" in research and isinstance(research["agregados"], list):
                for table in research["agregados"]:
                    final_table_list.append({
                        "id": table["id"],
                        "name": table["nome"] # Keeping original Portuguese name for user selection
                    })

        # Sort by table ID (as integer)
        return sorted(final_table_list, key=lambda x: int(x['id']))
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API to fetch tables: {e}")
        return None

@st.cache_data
def fetch_table_metadata(table_id: int) -> Optional[Dict[str, Any]]:
    """Fetches the metadata (variables, levels, periods) for a specific table ID."""
    try:
        response = requests.get(f"{API_URL}/sidra/tables/{table_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def fetch_sidra_data(params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """ Fetches specific consultation data from the API based on user parameters. """
    try:
        response = requests.get(f"{API_URL}/sidra/tables/fetch-specific", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Error fetching data from the API.")
        if e.response is not None:
            try:
                st.json(e.response.json())
            except:
                st.write(f"Error details: {e}")
        return None

def fetch_birthrate_map(state_abbr: str, year: int, metric_column: str) -> Optional[bytes]:
    """ Requests the birth rate map image from the backend API. """
    base_url = f"{API_URL}/maps/{state_abbr}/{year}/birth-rate"

    params = {
        "metric": metric_column,
        "group_code": "DN" # Declaração de Nascidos
    }

    st.info(f"Calling API: {base_url} with metric: {metric_column}")

    try:
        response = requests.get(base_url, params=params, timeout=60)
        response.raise_for_status()
        return response.content
        # response.content contains the raw bytes (PNG image) from the backend
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error generating map in the API.")
        if e.response is not None:
              try:
                  error_detail = e.response.json().get("detail", e.response.text)
                  st.write(f"Server error details: {error_detail}")
              except:
                  st.write(f"Network error details: {e}")
        return None
    
@st.cache_data
def fetch_pysus_systems() -> Optional[List[Dict[str, Any]]]:
    """Fetches the list of all supported PySUS systems from the API."""
    try:
        response = requests.get(f"{API_URL}/pysus/systems/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API to fetch PySUS systems: {e}")
        return None

@st.cache_data
def fetch_sinan_variables() -> Optional[Dict[str, Any]]:
    """Fetches the list of variables (diseases/conditions) available for SINAN."""
    try:
        response = requests.get(f"{API_URL}/pysus/sinan/variables")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API to fetch SINAN variables: {e}")
        return None
def fetch_sinan_data(params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Requests a summary of SINAN data from the API based on disease, year, and state."""
    
    # A API espera os anos e estados como listas, que já estão no dicionário 'params'
    base_url = f"{API_URL}/pysus/sinan/fetch-data"

    st.info(f"Sending query to API: {base_url} with parameters: {params}")
    
    try:
        # Nota: O 'requests' lida automaticamente com listas nos parâmetros (years=[2022] vira ?years=2022)
        response = requests.get(base_url, params=params, timeout=120) 
        response.raise_for_status()
        
        # O backend retorna uma lista de dicionários (o sumário de casos)
        return response.json() 
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching SINAN data from the API.")
        if e.response is not None:
              try:
                  error_detail = e.response.json().get("detail", e.response.text)
                  st.write(f"Server error details: {error_detail}")
              except:
                  st.write(f"Network error details: {e}")
        return None