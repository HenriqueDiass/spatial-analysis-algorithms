import pandas as pd
import geopandas as gpd
from typing import List, Dict, Optional, Any
# Certifique-se de que esta importação existe no seu projeto:
from src.infrastructure.shared.geography_utils import fetch_municipalities_gdf 

class PrevalenceDataProcessor:
    
    def __init__(self, year: int = 2022):
        self._year = year 
        
    def _process_sinan_summary(self, sinan_summary: List[Dict[str, Any]]) -> pd.DataFrame:
        """ 
        Converte o sumário do SINAN (lista de dicts) em um DataFrame 
        pronto para o merge, garantindo o tipo correto da chave.
        """
        
        if not sinan_summary:
            return pd.DataFrame(columns=['code_muni_6digit', 'total_cases'])
            
        cases_df = pd.DataFrame(sinan_summary)
        
        cases_df = cases_df.rename(columns={'municipality_code': 'code_muni_6digit'})
        
        cases_df['code_muni_6digit'] = pd.to_numeric(
            cases_df['code_muni_6digit'], 
            errors='coerce' 
        )
        
        cases_df = cases_df.dropna(subset=['code_muni_6digit'])
        
        cases_df['code_muni_6digit'] = cases_df['code_muni_6digit'].astype(int)
        
        return cases_df[['code_muni_6digit', 'total_cases']]

    def execute(
        self, 
        state_abbr: str, 
        population_data: List[Dict[str, Any]], 
        sinan_summary: List[Dict[str, Any]],
        multiplier: int = 100_000 
    ) -> Optional[gpd.GeoDataFrame]:
        
        print(" -> [Processador] Buscando geometrias...")
        municipalities_gdf = fetch_municipalities_gdf(state_abbr, self._year)
        if municipalities_gdf is None: 
            print("Erro: Não foi possível buscar as geometrias.")
            return None
        
        print(" -> [Processador] Processando dados de casos (SINAN)...")
        cases_df = self._process_sinan_summary(sinan_summary)
        
        print(" -> [Processador] Processando dados de população...")
        population_df = pd.DataFrame(population_data)
        if 'code_muni_6digit' in population_df.columns:
             population_df['code_muni_6digit'] = population_df['code_muni_6digit'].astype(int)
        else:
             print("Erro: 'code_muni_6digit' não encontrado nos dados de população.")
             return None

        numeric_cols_to_clean = ['total_cases', 'population']
        
        print(" -> [Processador] Unindo dados geo, casos e população...")
        merged_gdf = municipalities_gdf.merge(
            cases_df, 
            on='code_muni_6digit', 
            how='left' 
        )
        
        merged_gdf = merged_gdf.merge(
            population_df[['code_muni_6digit', 'population']], 
            on='code_muni_6digit', 
            how='left' 
        )
        
        merged_gdf[numeric_cols_to_clean] = merged_gdf[numeric_cols_to_clean].fillna(0).astype(int)

        rate_column_name = f'prevalence_per_{multiplier}'
        merged_gdf[rate_column_name] = 0.0 
        
        valid_population_mask = merged_gdf['population'] > 0
        
        merged_gdf.loc[valid_population_mask, rate_column_name] = \
            (merged_gdf.loc[valid_population_mask, 'total_cases'] / merged_gdf.loc[valid_population_mask, 'population']) * multiplier
        
        print(f" -> [Processador] ✅ Dados processados e GeoDataFrame criado. (Taxa: {rate_column_name})")
        return merged_gdf