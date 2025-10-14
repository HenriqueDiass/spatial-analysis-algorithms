import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import geopandas as gpd
import geobr

from shared.map_components import map_styles

def plot(
    gdf: gpd.GeoDataFrame,
    state_abbr: str,
    column_to_plot: str,
    title: str,
    legend_label: str,
    output_path: str
) -> bool:
    """
    Recebe um GeoDataFrame e plota um mapa coroplético com fundo de contexto,
    utilizando o esquema de estilo centralizado.
    """
    print(f"\n--- [Visualização] Iniciando desenho do mapa: '{title}' ---")
    
    try:
        style = map_styles.STYLES['advanced_choropleth']
        
        print(" -> [Visualização] Buscando mapa do Brasil para usar como fundo...")
        brasil_gdf = geobr.read_state(year=2020)
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 12), facecolor=style['figure']['facecolor'])
        ax.set_aspect('equal')

        # --- DESENHANDO AS CAMADAS ---
        print(" -> [Visualização] Desenhando camada de fundo (zorder=1)...")
        brasil_gdf.plot(
            ax=ax,
            color=style['context_layer']['facecolor'],
            edgecolor=style['context_layer']['edgecolor'],
            linewidth=style['context_layer']['linewidth'],
            zorder=1
        )

        print(f" -> [Visualização] Desenhando mapa coroplético de {state_abbr} (zorder=2)...")
        gdf[column_to_plot] = gdf[column_to_plot].fillna(0)
        vmax = gdf[column_to_plot].quantile(0.95)
        if vmax == 0: vmax = 10

        gdf.plot(
            ax=ax, 
            column=column_to_plot, 
            cmap=style['choropleth_layer']['cmap'],
            linewidth=style['choropleth_layer']['linewidth'],
            edgecolor=style['choropleth_layer']['edgecolor'],
            legend=True, 
            vmin=0, 
            vmax=vmax,
            zorder=2,
            legend_kwds={'label': legend_label, 'orientation': "horizontal", 'shrink': 0.6, 'pad': 0.05}
        )

        # --- AJUSTE DE ZOOM E FINALIZAÇÃO ---
        print(" -> [Visualização] Ajustando zoom e finalizando o mapa...")
        state_boundary = brasil_gdf[brasil_gdf['abbrev_state'] == state_abbr.upper()]
        if not state_boundary.empty:
            minx, miny, maxx, maxy = state_boundary.total_bounds
            buffer_x = (maxx - minx) * 0.20
            buffer_y = (maxy - miny) * 0.20
            ax.set_xlim(minx - buffer_x, maxx + buffer_x)
            ax.set_ylim(miny - buffer_y, maxy + buffer_y)

        # ADICIONA O CONTORNO ANTES DE DESLIGAR OS EIXOS
        rect = patches.Rectangle(
            (0, 0), 1, 1, 
            transform=ax.transAxes,
            linewidth=1.5,
            edgecolor='black',
            facecolor='none',
            zorder=10
        )
        ax.add_patch(rect)

        ax.set_axis_off()
        ax.set_title(title, fontdict=style['title'], pad=20)
        
        output_dir = os.path.dirname(output_path)
        if output_dir: os.makedirs(output_dir, exist_ok=True)
        
        print(f" -> [Visualização] Salvando mapa em '{os.path.basename(output_path)}'...")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        print(f"--- [Visualização] ✅ Mapa salvo com sucesso em '{output_path}'! ---")
        return True

    except Exception as e:
        print(f"❌ ERRO ao gerar a imagem do mapa: {e}")
        if 'fig' in locals(): plt.close(fig)
        return False