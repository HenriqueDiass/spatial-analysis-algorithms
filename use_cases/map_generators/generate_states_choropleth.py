# use_cases/map_generators/generate_states_choropleth.py
import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from shared.map_components import create_base_map, plot_choropleth_layer
from shared.map_components import map_styles

def execute(coluna: str, caminhos: dict) -> None:
    print(f"\n--- Caso de Uso: Gerando Mapa Coroplético de Estados por '{coluna}' ---")
    
    projecao: str = "epsg:3857"
    print("  -> Preparando dados geográficos...")
    try:
        gdf_estados = gpd.read_file(caminhos['estados']).to_crs(projecao)
    except Exception as e:
        print(f"  -> ERRO: Falha ao carregar o arquivo de estados. Erro: {e}")
        return

    print("\n  -> Orquestrando a plotagem das camadas do mapa...")
    
    choropleth_style = map_styles.STYLES['state_choropleth']
    general_style = map_styles.GENERAL_STYLE
    
    fig, ax = create_base_map(caminhos['sulamerica'])
    
    plot_choropleth_layer(
        ax, 
        geodataframe=gdf_estados, 
        data_column=coluna, 
        cmap=choropleth_style['cmap'],
        zorder=2
    )

    print("  -> Finalizando e salvando o mapa...")
    ax.set_title(
        f"Mapa Coroplético dos Estados por '{coluna.capitalize()}'", 
        fontsize=general_style['title_fontsize'],
        color=general_style['title_color_on_light_bg']
    )
    fig.patch.set_facecolor(general_style['figure_background_color'])
    
    plt.savefig(caminhos['saida'], dpi=300, bbox_inches='tight', pad_inches=0.05)
    print(f"--- Tarefa Concluída! Mapa salvo como '{os.path.basename(caminhos['saida'])}' ---")
    plt.close(fig)