# use_cases/__init__.py

# Importa a classe principal de cada sub-pacote
from .fetch_immediate_regions import FetchImmediateRegionsUseCase
from .fetch_intermediate_regions import FetchIntermediateRegionsUseCase
from .fetch_municipalities import FetchMunicipalitiesUseCase
from .fetch_states import FetchStatesUseCase 

# É uma boa prática definir '__all__' para controlar o que é importado
# quando alguém usa 'from use_cases import *'
__all__ = [
    'FetchImmediateRegionsUseCase',
    'FetchIntermediateRegionsUseCase',
    'FetchMunicipalitiesUseCase',
    'FetchStatesUseCase', 
]