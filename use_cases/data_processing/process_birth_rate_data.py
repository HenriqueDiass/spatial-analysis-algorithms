import os
import pandas as pd
import geopandas as gpd
import geobr
import json
from typing import Optional

def execute(
    state_abbr: str, 
    year: int, 
    sinasc_json_path: str, 
    population_json_path: str
) -> Optional[gpd.GeoDataFrame]:
    """
    Carrega dados brutos, une as fontes e calcula as taxas de natalidade
    e os totais por faixa etária da mãe.
    """
    print(f"\n--- [Processamento] Iniciando cálculo de taxas para {state_abbr} - {year} ---")
    
    if not all(os.path.exists(p) for p in [sinasc_json_path, population_json_path]):
        print("❌ ERRO: Arquivos de dados de entrada (SINASC ou População) não encontrados.")
        return None

    try:
        print(" -> [Processamento] Carregando e unindo fontes de dados...")
        gdf_mapa = geobr.read_municipality(code_muni=state_abbr, year=2020)
        gdf_mapa['code_muni_6digit'] = gdf_mapa['code_muni'] // 10

        print(" -> [Processamento] Carregando e processando dados de nascimentos (SINASC)...")
        with open(sinasc_json_path, "r", encoding="utf-8") as f:
            sinasc_data = json.load(f).get("summary_by_municipality", {})
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        # Extrai os dados por faixa etária além do total
        processed_data = []
        for mun_code, details in sinasc_data.items():
            age_data = details.get("by_faixa_etaria_mae", {})
            processed_data.append({
                'code_muni_6digit': int(mun_code), 
                'total_nascimentos': details.get('total', 0),
                'nascimentos_menor20': age_data.get('<20', 0),
                'nascimentos_20a29': age_data.get('20-29', 0),
                'nascimentos_30a39': age_data.get('30-39', 0),
                'nascimentos_40mais': age_data.get('40+', 0)
            })
        df_nascimentos = pd.DataFrame(processed_data)
        # --- FIM DA MUDANÇA ---

        print(" -> [Processamento] Carregando dados de população (JSON)...")
        df_populacao = pd.read_json(population_json_path, orient='records')

        gdf_final = gdf_mapa.merge(df_nascimentos, on='code_muni_6digit', how='left')
        gdf_final = gdf_final.merge(df_populacao[['code_muni_6digit', 'population']], on='code_muni_6digit', how='left')
        
        # Preenche com 0 todos os campos numéricos que não tiveram correspondência
        numeric_cols = [
            'total_nascimentos', 'population', 'nascimentos_menor20', 
            'nascimentos_20a29', 'nascimentos_30a39', 'nascimentos_40mais'
        ]
        for col in numeric_cols:
            gdf_final[col] = gdf_final[col].fillna(0).astype(int)

        print(" -> [Processamento] Calculando métricas...")
        gdf_final['taxa_natalidade_por_mil'] = 0.0
        mask = gdf_final['population'] > 0
        gdf_final.loc[mask, 'taxa_natalidade_por_mil'] = \
            (gdf_final.loc[mask, 'total_nascimentos'] / gdf_final.loc[mask, 'population']) * 1000

        print("--- [Processamento] ✅ Dados preparados com sucesso! ---")
        return gdf_final

    except Exception as e:
        print(f"❌ ERRO durante o processamento dos dados: {e}")
        return None