# src/domain/use-cases/pysus/sinasc/get-summary-sinasc.use-case.py
"""
Use case to fetch SINASC data and return an aggregated summary of births.
"""
import pandas as pd
from pysus.ftp.databases import SINASC
from typing import List, Dict, Any, Optional

from src.infrastructure.shared import data_utils

class GetSummarySinascUseCase:
    
    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None) -> Dict[str, Any]:
        
        # 1. Inicializa a variável do cabeçalho
        column_names: Optional[List[str]] = None 
        
        try:
            
            sinasc_db = SINASC().load()
            files_to_download = sinasc_db.get_files(group=group_code, year=years, uf=states)

            if not files_to_download:
                # 2. Atualiza o retorno para o novo formato
                return {"summary": {}, "columns": []} 
            
            downloaded_objects = sinasc_db.download(files_to_download)
            if not downloaded_objects:
                # 2. Atualiza o retorno para o novo formato
                return {"summary": {}, "columns": []} 

            if isinstance(downloaded_objects, list):
                list_of_dataframes = [pq.to_dataframe() for pq in downloaded_objects]
                unfiltered_dataframe = pd.concat(list_of_dataframes, ignore_index=True) if list_of_dataframes else pd.DataFrame()
            else:
                unfiltered_dataframe = downloaded_objects.to_dataframe()

            if unfiltered_dataframe.empty:
                return {"summary": {}, "columns": []} 

            
            column_names = unfiltered_dataframe.columns.tolist()
            print(f"-> Cabeçalho SINASC capturado: {column_names[:5]}...")
            

            filtered_dataframe = data_utils.filter_dataframe_by_states(
                unfiltered_dataframe, 
                states, 
                municipality_code_column='CODMUNNASC'
            )
            
            birth_summary = {}
            required_cols = ['IDADEMAE', 'CODMUNNASC', 'SEXO']
            
            if all(col in filtered_dataframe.columns for col in required_cols):

                processed_df = filtered_dataframe.dropna(subset=required_cols).copy()
                processed_df['mother_age_group'] = processed_df['IDADEMAE'].apply(data_utils.get_age_group)
                
                summary_df = processed_df.groupby(['CODMUNNASC', 'SEXO', 'mother_age_group']).size().reset_index(name='count')
                
                for _, row in summary_df.iterrows():
                    mun_code, sex, age_group, count = str(row['CODMUNNASC']), str(row['SEXO']), str(row['mother_age_group']), int(row['count'])
                    
                    if mun_code not in birth_summary:
                        birth_summary[mun_code] = {"total": 0, "by_sex": {}, "by_mother_age_group": {}}
                    
                    birth_summary[mun_code]["total"] += count
                    birth_summary[mun_code]["by_sex"][sex] = birth_summary[mun_code]["by_sex"].get(sex, 0) + count
                    birth_summary[mun_code]["by_mother_age_group"][age_group] = birth_summary[mun_code]["by_mother_age_group"].get(age_group, 0) + count
            
            
            return {
                "summary": birth_summary,
                "columns": column_names if column_names else []
            }

        except Exception as e:
            print(f"An error occurred during SINASC summary generation: {e}") 
            # 5. Atualiza o retorno de exceção
            return {"summary": {}, "columns": []}