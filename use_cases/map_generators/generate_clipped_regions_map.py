# use_cases/map_generators/generate_clipped_regions_map.py
import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from shared.map_components import create_base_map, plot_states_layer, plot_polygons_layer
from shared.map_components import map_styles

def execute(uf: str, caminhos: dict, region_type: str) -> None:
    print(f"\n--- Caso de Uso: Gerando Mapa de Regiões '{region_type.capitalize()}' para {uf} ---")
    
    if region_type == 'imediatas':
        region_path = caminhos['imediatas']
    elif region_type == 'intermediarias':
        region_path = caminhos['intermediarias']
    else:
        print(f"  -> ERRO: Tipo de região '{region_type}' inválido.")
        return

    projecao: str = "epsg:3857"
    print("  -> Preparando dados geográficos...")
    try:
        gdf_estados = gpd.read_file(caminhos['estados']).to_crs(projecao)
        mascara_estado = gdf_estados[gdf_estados['abbreviation'] == uf.upper()].copy()
        if mascara_estado.empty: 
            print(f"  -> ERRO: Estado '{uf}' não encontrado."); return
        mascara_estado['geometry'] = mascara_estado.geometry.buffer(0)

        gdf_regioes = gpd.read_file(region_path).to_crs(projecao)
        gdf_regioes['geometry'] = gdf_regioes.geometry.buffer(0)
        regioes_recortadas = gpd.clip(gdf_regioes, mascara_estado)
    except Exception as e:
        print(f"  -> ERRO: Falha durante a preparação dos dados. Erro: {e}")
        return

    print("\n  -> Orquestrando a plotagem das camadas do mapa...")
    
    clipped_styles = map_styles.STYLES['clipped_regions']
    general_style = map_styles.GENERAL_STYLE

    if region_type == 'imediatas':
        region_style = clipped_styles['immediate_region']
    else:
        region_style = clipped_styles['intermediate_region']
    
    final_border_style = clipped_styles['state_final_border']

    fig, ax = create_base_map(caminhos['sulamerica'])
    plot_states_layer(ax, gdf_estados, zorder=2)
    
    if not regioes_recortadas.empty:
        plot_polygons_layer(ax, regioes_recortadas, facecolor='none', **region_style, zorder=3)
    
    mascara_estado.plot(ax=ax, facecolor='none', **final_border_style, zorder=4)

    print("  -> Finalizando o mapa...")
    minx, miny, maxx, maxy = mascara_estado.total_bounds
    ax.set_xlim(minx - (maxx - minx) * 0.10, maxx + (maxx - minx) * 0.10)
    ax.set_ylim(miny - (maxy - miny) * 0.10, maxy + (maxy - miny) * 0.10)

    ax.set_title(
        f"Regiões {region_type.capitalize()} de {uf}", 
        fontsize=general_style['title_fontsize'],
        color=general_style['title_color_on_light_bg']
    )
    fig.patch.set_facecolor(general_style['figure_background_color'])
    ax.set_facecolor(general_style['map_background_color'])
    
    plt.savefig(caminhos['saida'], dpi=300, bbox_inches='tight', pad_inches=0.05)
    print(f"--- Tarefa Concluída! Mapa salvo como '{os.path.basename(caminhos['saida'])}' ---")
    plt.close(fig)