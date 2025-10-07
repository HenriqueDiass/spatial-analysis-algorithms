# src/domain/use-cases/sidrapy/fetch-tables-sidrapy.use-case.py
"""
Use case to fetch the complete list of available tables (aggregates) 
from the IBGE SIDRA API.
"""
import requests
from typing import List, Dict, Any, Optional

SIDRA_AGGREGATES_API_URL = 'https://servicodados.ibge.gov.br/api/v3/agregados'

class FetchTablesSidrapyUseCase:
   
    def execute(self) -> Optional[List[Dict[str, Any]]]:

        try:
            response = requests.get(SIDRA_AGGREGATES_API_URL, timeout=30)
            
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            
            print(f"An error occurred while fetching SIDRA tables: {e}") # In a real app, use logging.
            return None