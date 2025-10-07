# src/domain/use-cases/pysus/sih/get-variables-sih.use-case.py
"""
Use case to inspect the SIH data source and list its available data groups.
"""
from pysus.ftp.databases import SIH
from typing import List, Dict, Optional

class GetVariablesSihUseCase:

    def execute(self) -> Optional[List[Dict[str, str]]]:

        try:
            sih_db = SIH().load()

            if not sih_db.groups:
                print("Could not load SIH groups from PySUS.") 
                return None

            groups_list = [
                {"code": code, "name": description}
                for code, description in sih_db.groups.items()
            ]

            return groups_list

        except Exception as e:
            # For a real application, use a dedicated logger.
            print(f"An error occurred while fetching SIH variables: {e}")
            return None