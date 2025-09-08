# use_cases/map_generators/generate_highlight_map.py
import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from shared.map_components import create_base_map, plot_states_layer, plot_highlight_layer
from shared.map_components import map_styles

def execute(uf: str, caminhos: dict) -> None:
    print(f"\n--- Caso de Uso: Gerando Mapa de Destaque para {uf} ---")
    
    projecao: str = "epsg:3857"
    print("  -> Preparando dados geográficos...")
    try:
        gdf_estados = gpd.read_file(caminhos['estados']).to_crs(projecao)
    except Exception as e:
        print(f"  -> ERRO: Falha ao carregar o arquivo de estados. Erro: {e}")
        return

    print("  -> Orquestrando a plotagem das camadas do mapa...")
    
    general_style = map_styles.GENERAL_STYLE

    fig, ax = create_base_map(caminhos['sulamerica'])
    plot_states_layer(ax, gdf_estados, zorder=2)
    plot_highlight_layer(ax, gdf_estados, uf, zorder=3)
    
    print("  -> Finalizando e salvando o mapa...")
    ax.set_title(
        f'Destaque para o estado de {uf}', 
        fontsize=general_style['title_fontsize'],
        color=general_style['title_color_on_dark_bg']
    )

    plt.savefig(caminhos['saida'], dpi=300, bbox_inches='tight')
    print(f"--- Tarefa Concluída! Mapa salvo como '{os.path.basename(caminhos['saida'])}' ---")
    plt.close(fig)