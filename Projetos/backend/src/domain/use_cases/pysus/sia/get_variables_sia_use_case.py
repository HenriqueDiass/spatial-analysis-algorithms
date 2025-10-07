# src/domain/use-cases/pysus/sia/get-variables-sia.use-case.py
"""
Use case to inspect the SIA data source and list its available data groups.
"""
from pysus.ftp.databases import SIA
from typing import List, Dict, Optional

class GetVariablesSiaUseCase:
    def execute(self) -> Optional[List[Dict[str, str]]]:

        try:
            sia_db = SIA().load()

            if not sia_db.groups:
                print("Could not load SIA groups from PySUS.") # Log de erro
                return None

            groups_list = [
                {"code": code, "name": description}
                for code, description in sia_db.groups.items()
            ]
            return groups_list

        except Exception as e:

            print(f"An error occurred while fetching SIA variables: {e}")
            return None