import pandas as pd
from pysus.ftp.databases import SINAN
from typing import List, Dict, Optional
from collections import Counter
import pyarrow.parquet as pq
from pathlib import Path  

# Importa a versão atualizada com o filtro corrigido
from src.infrastructure.shared import data_utils 

class FetchDataSinanUseCase:
    
    def execute(self, disease_code: str, years: List[int], states: Optional[List[str]] = None) -> Optional[List[Dict]]:
        try:
            print(f"Buscando arquivos no SINAN para o agravo '{disease_code}'...")
            sinan_db = SINAN().load()
            total_counts = Counter()
            
            # Nota: Esta linha abaixo não é mais estritamente necessária aqui 
            # (já que a lógica de conversão está no data_utils.py), 
            # mas mantê-la não causa problemas.
            ibge_codes = [code for s in states if (code := data_utils.STATE_ABBR_TO_IBGE_CODE.get(s.upper()))] if states else []

            for year in years:
                print(f"Processando lote para o ano: {year}...")
                
                files_to_download = sinan_db.get_files(dis_code=disease_code, year=year)
                if not files_to_download: continue

                downloaded_obj = sinan_db.download(files_to_download, local_dir='/tmp')
                if not downloaded_obj: continue

                # --- LÓGICA FINAL: ENCONTRAR E LER OS ARQUIVOS DENTRO DA PASTA ---

                dir_path = Path(downloaded_obj.path)
                print(f"  -> Dados baixados na pasta: {dir_path}")

                parquet_files_paths = list(dir_path.glob('*.parquet'))
                
                if not parquet_files_paths:
                    print(f"  -> Nenhum arquivo .parquet encontrado dentro da pasta {dir_path}")
                    continue

                for filepath in parquet_files_paths:
                    print(f"    -> Lendo arquivo de dados: {filepath.name}")
                    parquet_file = pq.ParquetFile(filepath)

                    for i in range(parquet_file.num_row_groups):
                        chunk_df = parquet_file.read_row_group(i).to_pandas()
                        
                        if chunk_df.empty: continue

                        municipality_col = next((col for col in ["ID_MN_RESI", "ID_MUNICIP", "ID_MN_NOT"] if col in chunk_df.columns), None)
                        if not municipality_col: continue
                        
                        # CHAMADA DE FUNÇÃO MANTIDA. AGORA ELA FUNCIONA CORRETAMENTE!
                        filtered_chunk_df = data_utils.filter_dataframe_by_states(chunk_df, states, municipality_col)
                        
                        partial_counts = filtered_chunk_df.dropna(subset=[municipality_col])[municipality_col].value_counts()
                        total_counts.update(partial_counts.to_dict())
            
            # --- FIM DOS LOOPS ---
            
            if not total_counts:
                 print("Nenhum registro encontrado após o processamento.")
                 return None

            summary_list = [{"municipality_code": code, "total_cases": count} for code, count in total_counts.items()]
            print(f"Resumo final do SINAN gerado para {len(summary_list)} municípios.")
            
            return summary_list
            
        except Exception as e:
            print(f"Ocorreu um erro durante a busca de dados do SINAN: {e}")
            return None