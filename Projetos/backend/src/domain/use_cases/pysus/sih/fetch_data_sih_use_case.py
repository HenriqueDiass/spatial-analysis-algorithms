# src/domain/use_cases/pysus/sih/fetch_data_sih_use_case.py

import pandas as pd
from pysus.ftp.databases import SIH
from typing import List, Optional

class FetchDataSihUseCase:
 
    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None, months: Optional[List[int]] = None) -> Optional[pd.DataFrame]:

        try:
            print(f"Buscando dados no SIH para o grupo '{group_code}'...")
            sih_db = SIH().load()
            
            files_to_download = sih_db.get_files(
                group=group_code, 
                uf=states, 
                year=years, 
                month=months
            )

            if not files_to_download:
                print("Nenhum arquivo do SIH encontrado para os parâmetros.")
                return None

            downloaded_dataset = sih_db.download(files_to_download)
            
            if downloaded_dataset is None:
                return None

            dataframe = downloaded_dataset.to_dataframe()
            print(f"Processo do SIH concluído! {len(dataframe)} registros carregados.")
            return dataframe
            
        except Exception as e:
            print(f"Ocorreu um erro durante a busca de dados do SIH: {e}")
            return None