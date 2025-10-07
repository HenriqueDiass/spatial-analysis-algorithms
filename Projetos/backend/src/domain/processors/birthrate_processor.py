# src/domain/processors/birthrate_processor.py

import pandas as pd
import geopandas as gpd
from typing import List, Dict, Optional, Any
from src.infrastructure.shared.geography_utils import fetch_municipalities_gdf 
# Note: Certifique-se de que a linha de importação acima está correta para sua estrutura de pastas.


class BirthrateDataProcessor:
    
    def __init__(self, year: int = 2020):
        self._year = year 
        
    def _process_birth_summary(self, birth_summary: Dict[str, Any]) -> pd.DataFrame:
        """ 
        Converte o summary do SINASC em um DataFrame e cria as colunas de faixa etária 
        de forma eficiente, usando json_normalize.
        """
        
        # 1. Converte o dicionário principal em um DataFrame
        births_df = pd.DataFrame(
            [{
                # Limpa o código (removendo espaços) e o renomeia
                'code_muni_6digit': int(mun_code.strip()), 
                'total_births': details.get('total', 0),
                # Apenas mantemos o dicionário de faixa etária para a próxima etapa
                'age_groups': details.get("by_mother_age_group", {})
            }
            for mun_code, details in birth_summary.items()]
        )
        
        # 2. Normaliza a coluna 'age_groups'
        # Cria um DataFrame temporário (df_age) com as novas colunas: <20, 20-29, etc.
        # index=False impede que o índice (0, 1, 2...) seja incluído no resultado
        df_age = pd.json_normalize(
            births_df['age_groups'], 
            sep='_' # O separador não importa aqui, pois não há chaves duplicadas.
        )
        
        # 3. Renomeia as colunas do df_age para o seu padrão final
        df_age = df_age.rename(columns={
            '<20': 'births_mother_under20',
            '20-29': 'births_mother_20to29',
            '30-39': 'births_mother_30to39',
            '40+': 'births_mother_40plus'
        })
        
        # 4. Concatena (ou junta) os DataFrames. 
        # Como ambos têm o mesmo índice, o concat horizontal é o mais simples.
        result_df = pd.concat([
            births_df.drop(columns=['age_groups']), # Remove a coluna aninhada
            df_age.fillna(0).astype(int)            # Adiciona as colunas normalizadas e limpas
        ], axis=1)
        
        return result_df

    # O método execute e o init permanecem os mesmos
    # ...
    def execute(
        self, 
        state_abbr: str, 
        population_data: List[Dict[str, Any]], 
        birth_summary: Dict[str, Any]
    ) -> Optional[gpd.GeoDataFrame]:
        
        print(" -> [Processador] Buscando geometrias...")
        municipalities_gdf = fetch_municipalities_gdf(state_abbr, self._year)
        if municipalities_gdf is None: return None
        
        print(" -> [Processador] Processando dados de nascimentos...")
        births_df = self._process_birth_summary(birth_summary)
        population_df = pd.DataFrame(population_data)
        
        numeric_cols_to_clean = list(births_df.columns) + ['population']
        
        merged_gdf = municipalities_gdf.merge(births_df, on='code_muni_6digit', how='left')
        merged_gdf = merged_gdf.merge(population_df[['code_muni_6digit', 'population']], on='code_muni_6digit', how='left')
        
        merged_gdf[numeric_cols_to_clean] = merged_gdf[numeric_cols_to_clean].fillna(0).astype(int, errors='ignore')

        merged_gdf['birth_rate_per_1000'] = 0.0
        valid_population_mask = merged_gdf['population'] > 0
        merged_gdf.loc[valid_population_mask, 'birth_rate_per_1000'] = \
            (merged_gdf.loc[valid_population_mask, 'total_births'] / merged_gdf.loc[valid_population_mask, 'population']) * 1000
        
        print(" -> [Processador] ✅ Dados processados e GeoDataFrame criado.")
        return merged_gdf