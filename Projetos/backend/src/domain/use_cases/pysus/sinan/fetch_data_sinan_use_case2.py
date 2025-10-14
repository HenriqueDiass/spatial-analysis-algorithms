import pandas as pd
from pysus.ftp.databases import SINAN
from typing import List, Dict, Optional
from collections import Counter
# from src.infrastructure.shared import data_utils

class FetchDataSinanUseCase:
    """
    Busca dados do SINAN e retorna um resumo, processando os dados ano a ano
    para garantir baixo uso de memória.
    """
    def execute(self, disease_code: str = "ZIKA", years: List[int] = [2022], states: Optional[List[str]] = None) -> Optional[List[Dict]]:
        try:
            print(f"Buscando dados no SINAN para o agravo '{disease_code}'...")
            sinan_db = SINAN().load()
            total_counts = Counter()

            # --- LÓGICA CORRIGIDA: PROCESSAMENTO ANO A ANO ---
            # Em vez de baixar tudo de uma vez, fazemos um loop pelos anos.
            for year in years:
                print(f"Processando lote para o ano: {year}...")
                
                # 1. Baixa os dados para UM ano de cada vez.
                files_to_download = sinan_db.get_files(dis_code=disease_code, year=year)
                if not files_to_download:
                    print(f"  -> Nenhum arquivo encontrado para {year}. Pulando.")
                    continue

                downloaded_dataset = sinan_db.download(files_to_download)
                print(downloaded_dataset)

                dataframe = downloaded_dataset.to_dataframe()
                print(f"Processo do SIA concluído! {len(dataframe)} registros carregados.")
            
            return True
            
        except Exception as e:
            print(f"Ocorreu um erro durante a busca de dados do SINAN: {e}")
            return None
        
FetchDataSinanUseCase().execute()