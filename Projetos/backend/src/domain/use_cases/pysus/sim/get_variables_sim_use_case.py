# src/domain/use-cases/pysus/sim/get-variables-sim.use-case.py
"""
Use case to inspect the SIM data source and list its available data groups.
"""
from pysus import SIM
from typing import List, Dict, Optional

class GetVariablesSimUseCase:

    def execute(self) -> Optional[List[Dict[str, str]]]:
        try:
            sim_db = SIM().load()

            if not sim_db.groups:
                print("Could not load SIM groups from PySUS.") # Log de erro
                return None
            groups_list = [
                {"code": code, "name": description}
                for code, description in sim_db.groups.items()
            ]
            return groups_list

        except Exception as e:
            print(f"An error occurred while fetching SIM variables: {e}")
            return None