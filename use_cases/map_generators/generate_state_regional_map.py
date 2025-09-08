# use_cases/map_generators/generate_state_regional_map.py
import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from shared.map_components import create_base_map, plot_states_layer, plot_highlight_layer, plot_polygons_layer
from shared.map_components import map_styles

def execute(uf: str, caminhos: dict) -> None:
    print(f"\n--- Caso de Uso: Gerando Mapa de Divisões Regionais para {uf} ---")
    
    projecao: str = "epsg:3857"
    print("  -> Preparando dados geográficos...")
    try:
        gdf_estados = gpd.read_file(caminhos['estados']).to_crs(projecao)
        mascara_estado = gdf_estados[gdf_estados['abbreviation'] == uf.upper()].copy()
        if mascara_estado.empty: 
            print(f"  -> ERRO: Estado '{uf}' não encontrado."); return
        mascara_estado['geometry'] = mascara_estado.geometry.buffer(0)

        municipios_recortados = None
        if caminhos.get('municipios') and os.path.exists(caminhos['municipios']):
            gdf_municipios = gpd.read_file(caminhos['municipios']).to_crs(projecao)
            gdf_municipios['geometry'] = gdf_municipios.geometry.buffer(0)
            municipios_recortados = gpd.clip(gdf_municipios, mascara_estado)

        gdf_imediatas = gpd.read_file(caminhos['imediatas']).to_crs(projecao)
        gdf_imediatas['geometry'] = gdf_imediatas.geometry.buffer(0)
        imediatas_recortadas = gpd.clip(gdf_imediatas, mascara_estado)
        
        gdf_intermediarias = gpd.read_file(caminhos['intermediarias']).to_crs(projecao)
        gdf_intermediarias['geometry'] = gdf_intermediarias.geometry.buffer(0)
        intermediarias_recortadas = gpd.clip(gdf_intermediarias, mascara_estado)
    except Exception as e:
        print(f"  -> ERRO: Falha na preparação dos dados. Erro: {e}")
        return

    print("\n  -> Orquestrando a plotagem das camadas do mapa...")
    
    style = map_styles.STYLES['state_regional_map']
    general_style = map_styles.GENERAL_STYLE

    fig, ax = create_base_map(caminhos['sulamerica'])
    plot_states_layer(ax, gdf_estados, zorder=2)
    plot_highlight_layer(ax, gdf_estados, uf, zorder=3)
    
    if municipios_recortados is not None and not municipios_recortados.empty:
        plot_polygons_layer(ax, municipios_recortados, **style['municipality_coverage'], zorder=4)
        imediata_color = style['immediate_region_line']['edgecolor']
    else:
        mascara_estado.plot(ax=ax, color=style['municipality_coverage']['facecolor'], edgecolor='none', zorder=4)
        imediata_color = style['immediate_region_alt_color']

    plot_polygons_layer(ax, imediatas_recortadas, facecolor='none', edgecolor=imediata_color, linewidth=style['immediate_region_line']['linewidth'], zorder=5)
    plot_polygons_layer(ax, intermediarias_recortadas, facecolor='none', **style['intermediate_region_line'], zorder=5)
    mascara_estado.plot(ax=ax, facecolor='none', **style['final_border'], zorder=6)
    
    print("  -> Finalizando mapa...")
    minx, miny, maxx, maxy = mascara_estado.total_bounds
    ax.set_xlim(minx - (maxx - minx) * 0.05, maxx + (maxx - minx) * 0.05)
    ax.set_ylim(miny - (maxy - miny) * 0.05, maxy + (maxy - miny) * 0.05)

    legenda_intermediaria = mlines.Line2D([], [], color=style['intermediate_region_line']['edgecolor'], lw=1.8, label='Região Intermediária')
    legenda_imediata = mlines.Line2D([], [], color=imediata_color, lw=1.0, label='Região Imediata')
    ax.legend(handles=[legenda_intermediaria, legenda_imediata], loc='lower right', fontsize='small', facecolor='white', framealpha=0.8)

    ax.set_title(
        f"Divisões Regionais de {uf}", 
        fontsize=general_style['title_fontsize'], 
        color=general_style['title_color_on_light_bg']
    )
    
    plt.savefig(caminhos['saida'], dpi=300, bbox_inches='tight', pad_inches=0.05)
    print(f"--- Tarefa Concluída! Mapa salvo como '{os.path.basename(caminhos['saida'])}' ---")
    plt.close(fig)