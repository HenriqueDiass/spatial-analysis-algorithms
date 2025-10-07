# src/domain/use-cases/pysus/sim/fetch-data-sim.use-case.py
"""
Use case to fetch data from the SIM system, process it, and create a summary.
"""
import pandas as pd
from pysus.ftp.databases import SIM
from typing import List, Dict, Any, Optional, Tuple

from src.infrastructure.shared import data_utils

class FetchDataSimUseCase:
    """
    Orchestrates the download and processing of data from SIM (Sistema de 
    Informações sobre Mortalidade), including post-download filtering and summarization.
    """
    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None) -> Dict[str, Any]:

        try:
            sim_db = SIM().load()

            files_to_download = sim_db.get_files(group=group_code, year=years)

            if not files_to_download:
                return {"data": [], "summary_by_municipality": []}

            downloaded_objects = sim_db.download(files_to_download)
            if not downloaded_objects:
                 return {"data": [], "summary_by_municipality": []}
            
            if isinstance(downloaded_objects, list):
                list_of_dataframes = [pq.to_dataframe() for pq in downloaded_objects]
                unfiltered_dataframe = pd.concat(list_of_dataframes, ignore_index=True) if list_of_dataframes else pd.DataFrame()
            else:
                unfiltered_dataframe = downloaded_objects.to_dataframe()

            if unfiltered_dataframe.empty:
                return {"data": [], "summary_by_municipality": []}
            
            filtered_dataframe = data_utils.filter_dataframe_by_states(
                unfiltered_dataframe, 
                states, 
                municipality_code_column='CODMUNOCOR'
            )
            
            cases_per_municipality = []
            if 'CODMUNOCOR' in filtered_dataframe.columns:
                
                counts = filtered_dataframe.dropna(subset=['CODMUNOCOR'])['CODMUNOCOR'].value_counts()
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
            print(f"An error occurred during SIM data fetching: {e}") # Use logging in a real app
            return {"data": [], "summary_by_municipality": []}