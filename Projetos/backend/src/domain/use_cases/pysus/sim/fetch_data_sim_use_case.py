# src/domain/use-cases/pysus/sim/fetch-data-sim.use-case.py

import pandas as pd
from pysus.ftp.databases import SIM
from typing import List, Dict, Any, Optional
from collections import Counter
import pyarrow.parquet as pq
from pathlib import Path
import traceback 

from src.infrastructure.shared import data_utils 

class FetchDataSimUseCase:
    """
    Use case simplificado para o SIM, com chunking e filtragem de estado.
    """
    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None) -> Dict[str, Any]:
        
        total_counts = Counter()
        # 1. Variável do cabeçalho inicializada como None
        column_names: Optional[List[str]] = None 
        
        try:
            print("Carregando banco de dados SIM...")
            sim_db = SIM().load()

            state_prefixes = []
            if states:
                
                state_prefixes = [
                    data_utils.STATE_ABBR_TO_IBGE_CODE.get(st) 
                    for st in states if data_utils.STATE_ABBR_TO_IBGE_CODE.get(st)
                ]

            # 2. DOWNLOAD DOS ARQUIVOS
            download_params = {'group': group_code, 'year': years}
            if states:
                download_params['uf'] = states

            print(f"Buscando arquivos no SIM para os parâmetros: {download_params}")
            files_to_download = sim_db.get_files(**download_params)
            
            # 2. Retorno atualizado (se não houver arquivos)
            if not files_to_download: 
                return {"summary_by_municipality": [], "columns": []}

            downloaded_objects = sim_db.download(files_to_download, local_dir='/tmp')
            
            # 3. Retorno atualizado (se o download falhar)
            if not downloaded_objects: 
                return {"summary_by_municipality": [], "columns": []}
            
            
            if not isinstance(downloaded_objects, list):
                download_list_items = [downloaded_objects]
            else:
                download_list_items = downloaded_objects
            
            download_paths = [
                Path(item.path) if hasattr(item, 'path') else Path(str(item))
                for item in download_list_items
            ]
            
            for file_path in download_paths: 
                
                
                parquet_files_to_process = []
                if file_path.is_dir():
                    parquet_files_to_process.extend(list(file_path.glob('*.parquet')))
                elif file_path.is_file() and file_path.suffix == '.parquet':
                    parquet_files_to_process.append(file_path)

                if not parquet_files_to_process: continue
                
                for current_file_path in parquet_files_to_process:
                    if not current_file_path.is_file(): continue
                    
                    print(f"  -> Processando arquivo: {current_file_path.name}")
                    parquet_file = pq.ParquetFile(current_file_path)

                    # 4. Lógica de captura do cabeçalho (apenas uma vez)
                    if column_names is None:
                        column_names = parquet_file.schema.names #ccabe
                        print(f"-> Cabeçalho capturado: {column_names[:5]}...")

                    for i in range(parquet_file.num_row_groups):
                        chunk_table = parquet_file.read_row_group(i, columns=['CODMUNOCOR'])
                        chunk_df = chunk_table.to_pandas()
                        
                        if chunk_df.empty or 'CODMUNOCOR' not in chunk_df.columns: continue

                        
                        municipality_series = chunk_df.dropna(subset=['CODMUNOCOR'])['CODMUNOCOR'].astype(str).str.split('.').str[0]
                        
                        if state_prefixes:
                            municipality_prefix = municipality_series.str[0:2]
                            mask = municipality_prefix.isin(state_prefixes)
                            municipality_series = municipality_series[mask]
                            
                            if municipality_series.empty: continue

                        
                        partial_counts = municipality_series.value_counts()
                        total_counts.update(partial_counts.to_dict())
            
            
            if not total_counts:
                print("Nenhum óbito encontrado após o processamento.")
                # 5. Retorno atualizado (se não houver contagens)
                return {
                    "summary_by_municipality": [],
                    "columns": column_names if column_names else []
                }

            
            summary_list = [
                {"municipality_code": str(code), "total_deaths": int(count)}
                for code, count in total_counts.items()
            ]

            print(f"Sumário SIM gerado para {len(summary_list)} municípios.")

            # 6. Retorno principal (final) atualizado
            return {
                "summary_by_municipality": summary_list,
                "columns": column_names if column_names else []
            }

        except Exception as e:
            traceback.print_exc()
            print(f"Ocorreu um erro durante a busca de dados do SIM: {e}") 
            
            # 7. Retorno de exceção atualizado
            return {
                "summary_by_municipality": [],
                "columns": []
                
            }