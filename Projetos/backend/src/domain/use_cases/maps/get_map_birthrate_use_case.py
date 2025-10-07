# src/domain/use_cases/GetMapBirthrateUseCase.py

import io
from typing import Optional
import pandas as pd
import geobr

# Importa o novo processador
from src.domain.processors.birthrate_processor import BirthrateDataProcessor 

# Importa os outros UseCases
from src.domain.use_cases.ibge.population.fetch_data_population_use_case import FetchDataPopulationUseCase
from src.domain.use_cases.pysus.sinasc.get_summary_sinasc_use_case import GetSummarySinascUseCase
from src.infrastructure.shared import map_plotter


class GetMapBirthrateUseCase:
    """ 
    Orquestra a busca, processamento e visualização do mapa de taxa de natalidade.
    A responsabilidade de processamento de dados é delegada a BirthrateDataProcessor.
    """
    def execute(self, state_abbr: str, year: int, group_code: str, metric_column: str) -> Optional[io.BytesIO]:
        
        # --- PASSO 1: COLETAR DADOS (ORQUESTRAÇÃO) ---
        
        print("--- PASSO 1: COLETANDO DADOS ---")
        
        population_use_case = FetchDataPopulationUseCase()
        population_data = population_use_case.execute(year=year, state_abbr=state_abbr)
        if not population_data:
            print("❌ Falha: Dados de população não encontrados.")
            return None

        sinasc_use_case = GetSummarySinascUseCase()
        birth_summary = sinasc_use_case.execute(
            group_code=group_code,
            years=[year], 
            states=[state_abbr]
        )
        if not birth_summary:
            print("❌ Falha: Dados de nascimentos não encontrados.")
            return None

        # --- PASSO 2: PROCESSAR E COMBINAR (DELEGADO AO PROCESSOR) ---
        print("\n--- PASSO 2: PROCESSANDO DADOS ---")
        
        processor = BirthrateDataProcessor(year=2020) # Define o ano da geometria
        merged_gdf = processor.execute(
            state_abbr=state_abbr,
            population_data=population_data,
            birth_summary=birth_summary
        )
        
        if merged_gdf is None: return None
        

        # --- PASSO 3: GERAR A IMAGEM DO MAPA ---
        print("\n--- PASSO 3: GERANDO MAPA ---")
        
        metric_details = {
            "total_births": {"title": f"Total de Nascimentos - {state_abbr.upper()} ({year})", "label": "Nascimentos"},
            "birth_rate_per_1000": {"title": f"Taxa de Natalidade - {state_abbr.upper()} ({year})", "label": "Nasc. por 1.000 Hab."},
            "births_mother_under20": {"title": f"Nasc. de Mães com <20 anos - {state_abbr.upper()} ({year})", "label": "Nascimentos"},
            "births_mother_20to29": {"title": f"Nasc. de Mães com 20-29 anos - {state_abbr.upper()} ({year})", "label": "Nascimentos"},
            "births_mother_30to39": {"title": f"Nasc. de Mães com 30-39 anos - {state_abbr.upper()} ({year})", "label": "Nascimentos"},
            "births_mother_40plus": {"title": f"Nasc. de Mães com 40+ anos - {state_abbr.upper()} ({year})", "label": "Nascimentos"},
        }
        
        details = metric_details.get(metric_column)
        if not details:
            print(f"❌ Métrica '{metric_column}' inválida para este mapa.")
            return None

        image_buffer = map_plotter.plot_map(
            gdf=merged_gdf,
            state_abbr=state_abbr,
            column_to_plot=metric_column,
            title=details["title"],
            legend_label=details["label"]
        )

        return image_buffer