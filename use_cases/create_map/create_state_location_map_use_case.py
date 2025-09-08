# File: create_map/create_state_location_map_use_case.py

import os
import sys
import geobr
import matplotlib.pyplot as plt
import geopandas

# --- CONFIGURAÇÃO DE PATH E IMPORTAÇÕES CENTRALIZADAS ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from shared.map_components import map_styles

def execute(state_abbreviation: str, paths: dict):
    state_abbr = state_abbreviation.upper()
    print(f"\n--- Caso de Uso: Gerando mapa de destaque online para {state_abbr} ---")

    try:
        print(" -> Buscando dados geoespaciais do Brasil via geobr...")
        brazil_states_gdf = geobr.read_state(year=2020)
    
        print(f" -> Carregando mapa de fundo de '{os.path.basename(paths['sulamerica'])}'...")
        south_america_gdf = geopandas.read_file(paths['sulamerica'])
        
    except Exception as e:
        print(f"ERRO: Não foi possível carregar os dados necessários. Detalhes: {e}")
        return

    # --- STYLE CONFIGURATION (REMOVIDO!) ---
    # A configuração agora vem do nosso módulo central.
    style = map_styles.STYLES['online_highlight_map']

    # --- INICIANDO A CRIAÇÃO DO MAPA ---
    fig, ax = plt.subplots(1, 1, figsize=(10, 12), facecolor=style['figure_background'])
    ax.set_aspect('equal')

    # --- PLOTANDO AS CAMADAS ---
    
    # CAMADA 1: FUNDO
    print(" -> Desenhando camada de fundo: América do Sul (zorder=1)")
    south_america_gdf.plot(
        ax=ax, 
        color=style['south_america_fill'],
        edgecolor=style['south_america_edge'],
        zorder=1
    )

    # CAMADA 2: MEIO
    print(" -> Desenhando camada de dados: Estados do Brasil (zorder=2)")
    brazil_states_gdf.plot(
        ax=ax, 
        color=style['brazil_fill'],
        edgecolor=style['brazil_edge'], 
        linewidth=style['brazil_linewidth'], 
        zorder=2
    )

    # CAMADA 3: FRENTE (DESTAQUE)
    highlighted_state_gdf = brazil_states_gdf[brazil_states_gdf['abbrev_state'] == state_abbr]
    
    if not highlighted_state_gdf.empty:
        print(f" -> Desenhando camada de destaque: {state_abbr} (zorder=3)")
        highlighted_state_gdf.plot(
            ax=ax, 
            color=style['highlight_fill'],
            edgecolor=style['highlight_edge'],
            linewidth=style['highlight_linewidth'], 
            zorder=3
        )
    else:
        print(f"\nAVISO: Sigla '{state_abbr}' não encontrada nos dados do geobr. Mapa gerado sem destaque.")

    # --- FINALIZAÇÃO ---
    ax.set_xlim(-85, -30)
    ax.set_ylim(-57, 15)
    ax.set_axis_off()
    ax.set_title(
        f"Destaque para o Estado: {state_abbr}",
        fontdict=style['title']
    )

    output_path = paths['saida']
    print(f" -> Salvando mapa em '{os.path.basename(output_path)}'...")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    
    plt.close(fig)
    print("\n--- Mapa gerado e salvo com sucesso! ---")