# src/domain/use-cases/pysus/sinan/fetch-data-sinan.use-case.py
"""
Use case to fetch data from the SINAN system for a specific disease,
process it, and create a summary.
"""
import pandas as pd
from pysus.ftp.databases import SINAN
from typing import List, Dict, Any, Optional

from src.infrastructure.shared import data_utils

class FetchDataSinanUseCase:
    
    def execute(self, disease_code: str, years: List[int], states: Optional[List[str]] = None) -> Dict[str, Any]:
        try:
            sinan_db = SINAN().load()

            files_to_download = sinan_db.get_files(dis_code=disease_code, year=years)

            if not files_to_download:
                return {"data": [], "summary_by_municipality": []}

            downloaded_dataset = sinan_db.download(files_to_download)
            if not downloaded_dataset:
                return {"data": [], "summary_by_municipality": []}
            
            unfiltered_dataframe = downloaded_dataset.to_dataframe()
            if unfiltered_dataframe.empty:
                return {"data": [], "summary_by_municipality": []}

            municipality_col = next((col for col in ["ID_MN_RESI", "ID_MUNICIP", "ID_MN_NOT"] if col in unfiltered_dataframe.columns), None)
            
            filtered_dataframe = data_utils.filter_dataframe_by_states(
                unfiltered_dataframe, 
                states, 
                municipality_code_column=municipality_col
            ) if municipality_col else unfiltered_dataframe

            cases_per_municipality = []
            if municipality_col:
                counts = filtered_dataframe.dropna(subset=[municipality_col])[municipality_col].value_counts()
                cases_per_municipality = [
                    {"municipality_code": str(code), "total_cases": int(count)}
                    for code, count in counts.items()
                ]

            filtered_dataframe = filtered_dataframe.astype(object).where(pd.notnull(filtered_dataframe), None)
            
            return {
                "data": filtered_dataframe.to_dict(orient='records'),
                "summary_by_municipality": cases_per_municipality
            }

        except Exception as e:
            print(f"An error occurred during SINAN data fetching: {e}") 
            return {"data": [], "summary_by_municipality": []}