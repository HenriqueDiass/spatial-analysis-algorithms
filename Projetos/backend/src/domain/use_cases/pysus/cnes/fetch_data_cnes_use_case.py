# src/domain/use-cases/pysus/cnes/fetch-data-cnes.use-case.py
"""
Use case to fetch data from the CNES system using the PySUS library.
"""
import pandas as pd
from pysus.ftp.databases import CNES
from typing import List, Dict, Any, Optional

class FetchDataCnesUseCase:
    
    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        try:
            cnes_db = CNES().load()
            files_to_download = cnes_db.get_files(group=group_code, uf=states, year=years)

            if not files_to_download:
                return []

            downloaded_objects = cnes_db.download(files_to_download)
            list_of_dataframes = [parquet_object.to_dataframe() for parquet_object in downloaded_objects]
            
            if not list_of_dataframes:
                return []
            
            consolidated_dataframe = pd.concat(list_of_dataframes, ignore_index=True)
            
            consolidated_dataframe = consolidated_dataframe.astype(object).where(pd.notnull(consolidated_dataframe), None)
            
            return consolidated_dataframe.to_dict(orient='records')
            
        except Exception as e:
            print(f"An error occurred during CNES data fetching: {e}") # In a real app, this would be `logging.error(...)`
            return []