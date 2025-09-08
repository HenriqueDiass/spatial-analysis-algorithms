# Fetchers GeoBR
from .fetch_states.index import FetchStatesUseCase
from .fetch_municipalities.index import FetchMunicipalitiesUseCase
from .fetch_immediate_regions.index import FetchImmediateRegionsUseCase
from .fetch_intermediate_regions.index import FetchIntermediateRegionsUseCase

# Módulos de Mapa
from .create_map import gerar_mapa_destaque_geobr
# ATENÇÃO: As importações de 'discovery' foram REMOVIDAS daqui.

__all__ = [
    # Fetchers
    'FetchStatesUseCase',
    'FetchMunicipalitiesUseCase',
    'FetchImmediateRegionsUseCase',
    'FetchIntermediateRegionsUseCase',
    
    # ATENÇÃO: 'listers' e 'inspectors' REMOVIDOS daqui também.
    
    # Mapas
    'gerar_mapa_destaque_geobr',
]