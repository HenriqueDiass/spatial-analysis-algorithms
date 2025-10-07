# src/infrastructure/shared/geography_utils.py

import geopandas as gpd
import geobr
from typing import Optional

def fetch_municipalities_gdf(state_abbr: str, year: int = 2020) -> Optional[gpd.GeoDataFrame]:
    """ 
    Busca as geometrias dos municípios para um determinado estado e ano usando geobr.
    
    Centraliza a lógica de busca e pré-processamento do código municipal.
    """
    print(f" -> [Geografia] Buscando geometrias municipais para {state_abbr.upper()} (Ano: {year})...")
    try:
        # Nota: O geobr usa o código do estado ou a sigla.
        municipalities_gdf = geobr.read_municipality(code_muni=state_abbr.upper(), year=year)
        
        # Ajusta o código do município para 6 dígitos para compatibilidade
        municipalities_gdf['code_muni_6digit'] = municipalities_gdf['code_muni'] // 10
        return municipalities_gdf
    except Exception as e:
        print(f"❌ [Geografia] Falha ao buscar shapes do geobr: {e}")
        return None