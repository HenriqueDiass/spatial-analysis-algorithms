# use_cases/map_generators/generate_zoom_map.py
import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from shared.map_components import create_base_map, plot_states_layer, plot_highlight_layer, plot_polygons_layer
from shared.map_components import map_styles

def execute(uf: str, caminhos: dict) -> None:
    print(f"\n--- Caso de Uso: Gerando Mapa com Zoom para {uf} ---")
    
    projecao: str = "epsg:3857"
    print("  -> Preparando dados geográficos...")
    try:
        gdf_estados = gpd.read_file(caminhos['estados']).to_crs(projecao)
        mascara_estado = gdf_estados[gdf_estados['abbreviation'] == uf.upper()].copy()
        if mascara_estado.empty:
            print(f"  -> ERRO: Estado '{uf}' não encontrado."); return
        mascara_estado['geometry'] = mascara_estado.geometry.buffer(0)

        gdf_municipios = gpd.read_file(caminhos['municipios']).to_crs(projecao)
        gdf_municipios['geometry'] = gdf_municipios.geometry.buffer(0)
        municipios_do_estado = gpd.clip(gdf_municipios, mascara_estado)
    except Exception as e:
        print(f"  -> ERRO: Falha ao carregar ou processar arquivos. Erro: {e}")
        return

    print("\n  -> Orquestrando a plotagem das camadas do mapa...")
    
    zoom_style = map_styles.STYLES['zoom_map']
    general_style = map_styles.GENERAL_STYLE

    fig, ax = create_base_map(caminhos['sulamerica'])
    plot_states_layer(ax, gdf_estados, zorder=2)
    plot_highlight_layer(ax, gdf_estados, uf, zorder=3)
    
    plot_polygons_layer(
        ax, 
        municipios_do_estado, 
        **zoom_style['municipality_polygons'],
        zorder=4
    )

    print("  -> Finalizando mapa...")
    minx, miny, maxx, maxy = mascara_estado.total_bounds
    ax.set_xlim(minx - (maxx - minx) * 0.10, maxx + (maxx - minx) * 0.10)
    ax.set_ylim(miny - (maxy - miny) * 0.10, maxy + (maxy - miny) * 0.10)

    ax.set_title(
        f'Municípios de {uf}', 
        fontsize=general_style['title_fontsize'],
        color=general_style['title_color_on_light_bg']
    )
    fig.patch.set_facecolor(general_style['figure_background_color'])
    ax.set_facecolor(general_style['map_background_color'])
    
    plt.savefig(caminhos['saida'], dpi=300, bbox_inches='tight')
    print(f"--- Tarefa Concluída! Mapa salvo como '{os.path.basename(caminhos['saida'])}' ---")
    plt.close(fig)