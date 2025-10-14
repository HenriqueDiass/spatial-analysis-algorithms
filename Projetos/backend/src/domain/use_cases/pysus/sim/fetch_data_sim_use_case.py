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
        
        try:
            print("Carregando banco de dados SIM...")
            sim_db = SIM().load()

            # 1. PREPARAÇÃO DO FILTRO DE ESTADO (Prefixos IBGE)
            state_prefixes = []
            if states:
                # O states passado para o execute JÁ está em uppercase graças ao Controller
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
            if not files_to_download: return {"summary_by_municipality": []}

            downloaded_objects = sim_db.download(files_to_download, local_dir='/tmp')
            if not downloaded_objects: return {"summary_by_municipality": []}
            
            # --- OBTENÇÃO SIMPLIFICADA DOS CAMINHOS ---
            # Garante lista de Path objects a partir dos retornos ambíguos do pysus
            if not isinstance(downloaded_objects, list):
                download_list_items = [downloaded_objects]
            else:
                download_list_items = downloaded_objects
            
            download_paths = [
                Path(item.path) if hasattr(item, 'path') else Path(str(item))
                for item in download_list_items
            ]
            # ----------------------------------------

            # 3. PROCESSAMENTO POR CHUNKS (Mantém a lógica de SINAN)
            for file_path in download_paths: 
                
                # Lógica robusta para lidar com PASTA ou ARQUIVO direto
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

                    for i in range(parquet_file.num_row_groups):
                        chunk_table = parquet_file.read_row_group(i, columns=['CODMUNOCOR'])
                        chunk_df = chunk_table.to_pandas()
                        
                        if chunk_df.empty or 'CODMUNOCOR' not in chunk_df.columns: continue

                        # --- APLICAÇÃO DO FILTRO DE ESTADO E LIMPEZA ---
                        
                        # 1. Prepara a coluna do código do município (limpa .0 e filtra Nulos)
                        municipality_series = chunk_df.dropna(subset=['CODMUNOCOR'])['CODMUNOCOR'].astype(str).str.split('.').str[0]
                        
                        # 2. Aplica o filtro por prefixo IBGE
                        if state_prefixes:
                            municipality_prefix = municipality_series.str[0:2]
                            mask = municipality_prefix.isin(state_prefixes)
                            municipality_series = municipality_series[mask]
                            
                            if municipality_series.empty: continue

                        # 3. Conta e atualiza o contador
                        partial_counts = municipality_series.value_counts()
                        total_counts.update(partial_counts.to_dict())
            
            # --- FIM DO PROCESSAMENTO ---
            
            if not total_counts:
                print("Nenhum óbito encontrado após o processamento.")
                return {"summary_by_municipality": []}

            # 4. Formata a saída
            summary_list = [
                {"municipality_code": str(code), "total_deaths": int(count)}
                for code, count in total_counts.items()
            ]

            print(f"Sumário SIM gerado para {len(summary_list)} municípios.")

            return {"summary_by_municipality": summary_list}

        except Exception as e:
            traceback.print_exc()
            print(f"Ocorreu um erro durante a busca de dados do SIM: {e}") 
            return {"summary_by_municipality": []}