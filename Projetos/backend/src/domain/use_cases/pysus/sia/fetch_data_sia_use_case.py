# src/domain/use_cases/pysus/sia/fetch_data_sia_use_case.py

import pandas as pd
from pysus.ftp.databases import SIA
from typing import List, Optional

class FetchDataSiaUseCase:

    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None, months: Optional[List[int]] = None) -> Optional[pd.DataFrame]:

        try:
            print(f"Buscando dados no SIA para o grupo '{group_code}'...")
            sia_db = SIA().load()
            
            files_to_download = sia_db.get_files(
                group=group_code, 
                uf=states, 
                year=years, 
                month=months
            )

            if not files_to_download:
                print("Nenhum arquivo do SIA encontrado para os parâmetros.")
                return None

            downloaded_dataset = sia_db.download(files_to_download)
            
            if downloaded_dataset is None:
                return None

            dataframe = downloaded_dataset.to_dataframe()
            print(f"Processo do SIA concluído! {len(dataframe)} registros carregados.")
            return dataframe
            
        except Exception as e:
            print(f"Ocorreu um erro durante a busca de dados do SIA: {e}")
            return None