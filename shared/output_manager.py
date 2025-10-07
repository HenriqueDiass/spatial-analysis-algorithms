import os
import json
import pandas as pd
from . import pysus_tools  # Supondo que a função esteja em pysus_tools
from typing import Dict, Any, Tuple, List

# =============================================================================
# FUNÇÃO GENÉRICA PARA SALVAR RESUMOS
# =============================================================================

def save_summary_output(
    system_name: str,
    output_dir: str,
    filename: str,
    df: pd.DataFrame,
    metadata: Dict[str, Any]
):
    """Função centralizada para verificar e salvar a saída de resumo."""
    if df is None or df.empty:
        print(f"\nNenhum dado do {system_name} foi retornado. O arquivo JSON não foi gerado.")
        return

    full_path = os.path.join(output_dir, filename)
    
    # Chama a função principal com summary_only=True
    pysus_tools.save_data_to_json(
        dataframe=df,
        system_name=system_name,
        output_filename=full_path,
        metadata=metadata,
        summary_only=True  # <-- AQUI ESTÁ A MÁGICA!
    )

# =============================================================================
# GERENCIADORES ESPECIALIZADOS (AGORA MAIS SIMPLES)
# =============================================================================

def save_sinan_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, list, str]):
    """Organiza e salva o resumo de saída para o SINAN."""
    df, cases_per_municipality, filter_info = data_results
    filename = f"pysus_sinan_{params['disease_code']}_{'_'.join(map(str, params['years']))}.json"
    metadata = {
        "disease": params["disease_code"], "years": params["years"], "state": params["state"] or "Todos",
        "filter_info": filter_info, "cases_per_municipality": cases_per_municipality
    }
    save_summary_output("SINAN", output_dir, filename, df, metadata)

def save_sim_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, list]):
    """Organiza e salva o resumo de saída para o SIM."""
    df, cases_per_municipality = data_results
    filename = f"pysus_sim_{params['group_code']}_{'_'.join(map(str, params['years']))}.json"
    metadata = {
        "group": params["group_code"], "years": params["years"], "states": params["states"] or "Todos",
        "cases_per_municipality": cases_per_municipality
    }
    save_summary_output("SIM", output_dir, filename, df, metadata)

def save_sinasc_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, dict]):
    """Organiza e salva o resumo de saída para o SINASC."""
    df, summary_dict = data_results
    states_str = "_".join(params.get('states') or ['BR'])
    years_str = "_".join(map(str, params.get('years')))
    filename = f"pysus_sinasc_summary_{params['group_code']}_{years_str}_{states_str}.json"
    metadata = {
        "parameters": {
            "group": params["group_code"],
            "years": params["years"],
            "states": params["states"] or "Todos"
        },
        "summary_by_municipality": summary_dict
    }
    save_summary_output("SINASC", output_dir, filename, df, metadata)


def save_simple_output(system_name: str, output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    """Função genérica para sistemas sem agregações (CNES, SIA, SIH)."""
    years_str = '_'.join(map(str, params.get('years', [])))
    filename = f"pysus_{system_name.lower()}_{params.get('group_code', '')}_{years_str}.json"
    # Para sistemas simples, os próprios parâmetros podem ser os metadados
    metadata = params.copy()
    save_summary_output(system_name, output_dir, filename, df, metadata)


# Funções que apenas chamam a 'save_simple_output'
def save_cnes_output(output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    save_simple_output("CNES", output_dir, params, df)

def save_sia_output(output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    save_simple_output("SIA", output_dir, params, df)

def save_sih_output(output_dir: str, params: Dict[str, Any], df: pd.DataFrame):
    save_simple_output("SIH", output_dir, params, df)