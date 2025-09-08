# shared/output_manager.py

import os
import pandas as pd
from . import pysus_tools
from typing import Dict, Any, Tuple

# =============================================================================
# GERENCIADOR PARA SISTEMAS COM AGREGAÇÃO (SINAN, SIM, SINASC)
# =============================================================================

def save_sinan_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, list, str]):
    """Organiza e salva a saída para o SINAN, incluindo casos por município."""
    df, cases_per_municipality, filter_info = data_results
    if df is None or df.empty:
        print("\nNenhum dado foi retornado. O arquivo JSON não foi gerado.")
        return

    filename = f"pysus_sinan_{params['disease_code']}_{'_'.join(map(str, params['years']))}.json"
    full_path = os.path.join(output_dir, filename)
    metadata = {
        "disease": params["disease_code"], "years": params["years"], "state": params["state"] or "Todos",
        "filter_info": filter_info, "cases_per_municipality": cases_per_municipality
    }
    pysus_tools.save_data_to_json(df, "SINAN", full_path, metadata)

def save_sim_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, list]):
    """Organiza e salva a saída para o SIM, incluindo casos por município."""
    df, cases_per_municipality = data_results
    if df is None or df.empty:
        print("\nNenhum dado foi retornado. O arquivo JSON não foi gerado.")
        return

    filename = f"pysus_sim_{params['group_code']}_{'_'.join(map(str, params['years']))}.json"
    full_path = os.path.join(output_dir, filename)
    metadata = {
        "group": params["group_code"], "years": params["years"], "states": params["states"] or "Todos",
        "cases_per_municipality": cases_per_municipality
    }
    pysus_tools.save_data_to_json(df, "SIM", full_path, metadata)

def save_sinasc_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, dict]):
    """Organiza e salva a saída para o SINASC, incluindo a agregação complexa de casos."""
    df, cases_per_municipality = data_results
    if df is None or df.empty:
        print("\nNenhum dado foi retornado. O arquivo JSON não foi gerado.")
        return

    filename = f"pysus_sinasc_{params['group_code']}_{'_'.join(map(str, params['years']))}.json"
    full_path = os.path.join(output_dir, filename)
    metadata = {
        "group": params["group_code"], "years": params["years"], "states": params["states"] or "Todos",
        "cases_per_municipality": cases_per_municipality
    }
    pysus_tools.save_data_to_json(df, "SINASC", full_path, metadata)

# =============================================================================
# GERENCIADORES PARA SISTEMAS SIMPLES (CNES, SIA, SIH)
# =============================================================================

def save_simple_output(system_name: str, output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    """Função genérica para sistemas sem agregações customizadas (CNES, SIA, SIH)."""
    if df is None or df.empty:
        print(f"\nNenhum dado do {system_name} foi retornado. O arquivo JSON não foi gerado.")
        return

    years_str = '_'.join(map(str, params.get('years', [])))
    filename = f"pysus_{system_name.lower()}_{params.get('group_code', '')}_{years_str}.json"
    full_path = os.path.join(output_dir, filename)
    
    metadata = params.copy()
    pysus_tools.save_data_to_json(df, system_name, full_path, metadata)

def save_cnes_output(output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    """Função específica para o CNES que chama o salvamento simples."""
    save_simple_output("CNES", output_dir, params, df)

def save_sia_output(output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    """Função específica para o SIA que chama o salvamento simples."""
    save_simple_output("SIA", output_dir, params, df)

def save_sih_output(output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    """Função específica para o SIH que chama o salvamento simples."""
    save_simple_output("SIH", output_dir, params, df)