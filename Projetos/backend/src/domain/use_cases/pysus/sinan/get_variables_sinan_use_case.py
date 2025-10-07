# src/domain/use-cases/pysus/sinan/get-variables-sinan.use-case.py
"""
Use case to inspect the SINAN data source and list its available diseases/conditions.
"""
from pysus import SINAN
from typing import List, Dict, Optional

class GetVariablesSinanUseCase:
 
    def execute(self) -> Optional[List[Dict[str, str]]]:
       
        try:
            sinan_db = SINAN().load()

            if not sinan_db.diseases:
                print("Could not load SINAN diseases list from PySUS.") # Log de erro
                return None

            diseases_list = [
                {"code": code, "name": name}
                for code, name in sinan_db.diseases.items()
            ]

            return diseases_list

        except Exception as e:
            print(f"An error occurred while fetching SINAN variables: {e}")
            return None