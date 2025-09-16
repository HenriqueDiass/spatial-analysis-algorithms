# File: use_cases/create_map/gerar_mapa_pysus_coropleth.py

import os
import sys
import geobr
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from typing import List, Dict, Any

# --- CONFIGURAÇÃO DE PATH ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

from shared.map_components import map_styles

def get_nested_value(data: Dict[str, Any], keys: List[str]) -> int:
    """Navega por uma lista de chaves para obter um valor aninhado. Retorna 0 se o caminho não existir."""
    temp_data = data
    for key in keys:
        if isinstance(temp_data, dict):
            temp_data = temp_data.get(key)
        else:
            return 0
    return temp_data if isinstance(temp_data, (int, float)) else 0

def execute(
    data_dict: dict,
    state_abbr: str,
    output_path: str,
    data_keys: List[str],
    column_name: str,
    map_title: str,
    legend_label: str
):
    """
    Gera um mapa coroplético para os municípios de um estado com base em dados do PySUS.
    """
    state_abbr = state_abbr.upper()
    print(f"\n--- Gerando mapa coroplético para '{map_title}' ---")

    print(f" -> Extraindo dados para a coluna '{column_name}'...")
    map_data_list = [
        {'code_muni': int(mun_code), column_name: get_nested_value(details, data_keys)}
        for mun_code, details in data_dict.items()
    ]
    df_dados = pd.DataFrame(map_data_list)
    
    if df_dados.empty:
        print("AVISO: Dados de entrada vazios. Mapa não gerado."); return

    try:
        print(f" -> Buscando geometrias dos municípios de {state_abbr} via geobr...")
        gdf_municipios = geobr.read_municipality(code_muni=state_abbr, year=2020)
        
        print(" -> Unindo dados geoespaciais com os dados da aplicação...")
        gdf_merged = gdf_municipios.merge(df_dados, on='code_muni', how='left')
        gdf_merged[column_name] = gdf_merged[column_name].fillna(0)
    except Exception as e:
        print(f"ERRO: Falha ao processar dados geoespaciais. Detalhes: {e}"); return

    style = map_styles.STYLES.get('choropleth_map', {})
    fig, ax = plt.subplots(1, 1, figsize=(12, 10), facecolor=style.get('figure_background', 'white'))
    ax.set_aspect('equal')

    print(" -> Desenhando o mapa...")
    gdf_merged.plot(
        ax=ax, column=column_name, cmap='viridis', linewidth=0.5,
        edgecolor='white', legend=True,
        legend_kwds={'label': legend_label, 'orientation': "horizontal", 'shrink': 0.6}
    )

    ax.set_axis_off()
    ax.set_title(map_title, fontdict=style.get('title', {'fontsize': 16}))

    print(f" -> Salvando mapa em '{os.path.basename(output_path)}'...")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    print("\n--- Mapa gerado com sucesso! ---")