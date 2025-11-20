# src/domain/use-cases/pysus/sinasc/get-variables-sinasc.use-case.py
"""
Use case to inspect the SINASC data source and list its available data groups.
"""
from pysus import SINASC
from typing import List, Dict, Optional

class GetVariablesSinascUseCase:
    """
    This use case retrieves the available data groups from the SINASC
    (Sistema de Informações sobre Nascidos Vivos) database.
    """
    def execute(self) -> Optional[List[Dict[str, str]]]:
       
        try:
            
            sinasc_db = SINASC().load()

            if not sinasc_db.groups:
                print("Could not load SINASC groups from PySUS.") 
                return None

            groups_list = [
                {"code": code, "name": description}
                for code, description in sinasc_db.groups.items()
            ]

            return groups_list

        except Exception as e:
            # For a real application, use a dedicated logger.
            print(f"An error occurred while fetching SINASC variables: {e}")
            return None