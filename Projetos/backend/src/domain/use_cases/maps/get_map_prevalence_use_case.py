import io
from typing import Optional

from src.domain.processors.prevalence_processor import PrevalenceDataProcessor 
from src.domain.use_cases.ibge.population.fetch_data_population_use_case import FetchDataPopulationUseCase
from src.domain.use_cases.pysus.sinan.fetch_data_sinan_use_case import FetchDataSinanUseCase 
from src.infrastructure.shared import map_plotter

class GetMapPrevalenceUseCase:
    
    def execute(
        self, 
        state_abbr: str, 
        year: int, 
        disease_code: str,
        metric_column: str
    ) -> Optional[io.BytesIO]:
        
        # --- PASSO 1: COLETAR DADOS (ORQUESTRAÇÃO) ---
        print("--- PASSO 1: COLETANDO DADOS ---")
        
        population_use_case = FetchDataPopulationUseCase()
        population_data = population_use_case.execute(year=year, state_abbr=state_abbr)
        if not population_data:
            print("❌ Falha: Dados de população não encontrados.")
            return None

        sinan_use_case = FetchDataSinanUseCase()
        sinan_data_raw = sinan_use_case.execute(
            disease_code=disease_code,
            years=[year], 
            states=[state_abbr]
        )
        
        sinan_summary = sinan_data_raw.get('summary') if sinan_data_raw else None
        
        if not sinan_summary:
            print("❌ Falha: Dados de casos (SINAN) não encontrados.")
            return None

        # --- PASSO 2: PROCESSAR E COMBINAR (DELEGADO AO PROCESSOR) ---
        print("\n--- PASSO 2: PROCESSANDO DADOS ---")
        
        processor = PrevalenceDataProcessor(year=year) 
        
        merged_gdf = processor.execute(
            state_abbr=state_abbr,
            population_data=population_data,
            sinan_summary=sinan_summary
        )
        
        if merged_gdf is None: 
            print("❌ Falha: Não foi possível processar e unir os dados.")
            return None
        
        # --- PASSO 3: GERAR A IMAGEM DO MAPA ---
        print("\n--- PASSO 3: GERANDO MAPA ---")
        
        # O nome da coluna de taxa é 'prevalence_per_100000' (ou o multiplier usado)
        
        metric_details = {
            "total_cases": {
                "title": f"Total de Casos ({disease_code}) - {state_abbr.upper()} ({year})", 
                "label": "Nº de Casos"
            },
            "prevalence_per_100000": {
                "title": f"Prevalência ({disease_code}) - {state_abbr.upper()} ({year})", 
                "label": "Casos por 100.000 Hab."
            }
            # Adicione 'prevalence_per_1000' etc. se você mudar o multiplier
        }
        
        details = metric_details.get(metric_column)
        if not details:
            print(f"❌ Métrica '{metric_column}' inválida para este mapa.")
            print(f"   Métricas disponíveis: {list(metric_details.keys())}")
            return None

        image_buffer = map_plotter.plot_map(
            gdf=merged_gdf,
            state_abbr=state_abbr,
            column_to_plot=metric_column,
            title=details["title"],
            legend_label=details["label"]
        )

        return image_buffer