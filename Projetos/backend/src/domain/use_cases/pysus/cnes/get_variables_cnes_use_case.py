# src/domain/use-cases/pysus/cnes/get-variables-cnes.use-case.py
"""
Use case to inspect the CNES data source and list its available data groups.
"""
from pysus.ftp.databases import CNES
from typing import List, Dict, Optional

class GetVariablesCnesUseCase:
  
    def execute(self) -> Optional[List[Dict[str, str]]]:
        
        try:
            cnes_db = CNES().load()

            if not cnes_db.groups:
                print("Could not load CNES groups from PySUS.") # Log de erro
                return None
            
            groups_list = [
                {"code": code, "name": description}
                for code, description in cnes_db.groups.items()
            ]
            return groups_list

        except Exception as e:
            print(f"An error occurred while fetching CNES variables: {e}")
            return None