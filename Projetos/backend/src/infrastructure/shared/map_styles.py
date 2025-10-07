"""
Módulo centralizado para as configurações de estilo dos mapas.

Este arquivo é a fonte única de verdade para a aparência de todos os mapas.
A estrutura foi projetada para ser o mais clara e manutenível possível,
seguindo uma lógica de três passos:

1.  `COLOR_PALETTE`: Define as cores base do projeto. Mude uma cor aqui
    e ela se propagará por todos os estilos que a utilizam.

2.  `GENERAL_STYLE`: Define a aparência da "tela" do mapa, como cor de fundo
    e propriedades padrão dos títulos.

3.  `STYLES`: Um grande dicionário que contém as configurações detalhadas
    para cada tipo de mapa que seu programa pode gerar.
"""

# ==============================================================================
# 1. PALETA DE CORES PRINCIPAL
# ==============================================================================
# Define as cores centrais para a identidade visual do projeto.
COLOR_PALETTE = {
    # Cores primárias e temáticas
    'primary_blue': '#0077b6',
    'highlight_red': '#d00000',

    # Tons neutros para bordas, fundos e textos
    'neutral_dark': '#333333',
    'neutral_medium': '#d3d3d3',
    'neutral_light': '#f5f5f5',
    'missing_data': '#D3D3D3',

    # Cores padrão
    'white': '#ffffff',
    'black': '#000000',
}


# ==============================================================================
# 2. ESTILO GERAL DO MAPA
# ==============================================================================
# Configurações visuais padrão aplicadas à figura e aos eixos do Matplotlib.
GENERAL_STYLE = {
    'figure_background_color': COLOR_PALETTE['white'],
    'map_background_color': COLOR_PALETTE['white'],

    # Cores de título separadas para fundos claros ou escuros
    'title_color_on_light_bg': COLOR_PALETTE['black'],
    'title_color_on_dark_bg': COLOR_PALETTE['white'],
    'title_fontsize': 16,
}


# ==============================================================================
# 3. DICIONÁRIO DE ESTILOS ESPECÍFICOS
# ==============================================================================
# Agrupa todas as configurações de estilo para cada mapa em um único lugar.
# Cada chave neste dicionário corresponde a um tipo de mapa ou camada.

STYLES = {
    # Usado em: `generate_clipped_regions_map.py`
    'clipped_regions': {
        'immediate_region': {
            'edgecolor': COLOR_PALETTE['primary_blue'],
            'linewidth': 1.2,
        },
        'intermediate_region': {
            'edgecolor': COLOR_PALETTE['highlight_red'],
            'linewidth': 1.2,
        },
        'state_final_border': {
            'edgecolor': COLOR_PALETTE['black'],
            'linewidth': 0.8,
        }
    },

    # Usado em: `generate_highlight_map.py` e outras camadas de destaque
    'highlight_layer': {
        'facecolor': COLOR_PALETTE['highlight_red'],
        'edgecolor': COLOR_PALETTE['neutral_dark'],
        'linewidth': 1.0,
    },

    # Usado em: `generate_municipalities_choropleth.py`
    'municipality_choropleth': {
        'cmap': 'Blues',
        'linewidth': 0.5,
        'edgecolor': COLOR_PALETTE['neutral_dark'],
        'missing_kwds': {
            'color': COLOR_PALETTE['missing_data'],
            'label': 'Dados não disponíveis',
        }
    },

    # Usado em: `generate_states_choropleth.py`
    'state_choropleth': {
        'cmap': 'Blues',
        'linewidth': 0.7,
        'edgecolor': COLOR_PALETTE['black'],
        'missing_kwds': {
            'color': COLOR_PALETTE['missing_data'],
            'label': 'Dados não disponíveis',
        }
    },

    # Usado em: `generate_zoom_map.py`
    'zoom_map': {
        'municipality_polygons': {
            'facecolor': COLOR_PALETTE['neutral_light'],
            'edgecolor': COLOR_PALETTE['neutral_medium'],
            'linewidth': 0.3,
        }
    },

    # Usado em: `generate_state_regional_map.py`
    'state_regional_map': {
        'municipality_coverage': {
            'facecolor': COLOR_PALETTE['neutral_light'],
            'edgecolor': COLOR_PALETTE['neutral_medium'],
            'linewidth': 0.3,
        },
        'immediate_region_line': {
            'edgecolor': COLOR_PALETTE['primary_blue'],
            'linewidth': 1.0,
        },
        'immediate_region_alt_color': '#696969',
        'intermediate_region_line': {
            'edgecolor': COLOR_PALETTE['highlight_red'],
            'linewidth': 1.2,
        },
        'final_border': {
            'edgecolor': COLOR_PALETTE['black'],
            'linewidth': 0.8,
        }
    },
    
    # Usado em: `create_state_location_map_use_case.py`
    'online_highlight_map': {
        'figure_background': '#a6c9e2',
        'south_america_fill': '#f5f5f5',
        'south_america_edge': '#d3d3d3',
        'brazil_fill': '#f0e6c2',
        'brazil_edge': COLOR_PALETTE['white'],
        'brazil_linewidth': 0.7,
        'highlight_fill': COLOR_PALETTE['highlight_red'],
        'highlight_edge': COLOR_PALETTE['black'],
        'highlight_linewidth': 1.0,
        'title': {
            'fontsize': 16,
            'fontweight': 'bold',
            'color': COLOR_PALETTE['black']
        }
    },

    # <<< NOVO ESTILO ADICIONADO AQUI >>>
    # Estilo para o nosso novo mapa coroplético com fundo de contexto
    # Usado em: use_cases/create_map/plotter.py
    'advanced_choropleth': {
        'figure': {
            # Cor azul de fundo, vinda do seu estilo de destaque
            'facecolor': '#a6c9e2' 
        },
        'context_layer': {  # Estilo para o mapa do Brasil no fundo
            # Cor creme para o Brasil, vinda do seu estilo de destaque
            'facecolor': '#f0e6c2',
            # Borda branca, vinda do seu estilo de destaque
            'edgecolor': COLOR_PALETTE['black'], 
            'linewidth': 0.7,
        },
        'choropleth_layer': {  # Estilo para os municípios coloridos
            'cmap': 'Blues',#mos o gradiente de cores para os dados
            'linewidth': 0.5,
            'edgecolor': COLOR_PALETTE['black'], # Borda branca para consistência
        },
        'title': { # Estilo do título, idêntico ao do seu mapa de destaque
            'fontsize': 16,
            'fontweight': 'bold',
            'color': COLOR_PALETTE['black']
        }
    },
}