# src/domain/use_cases/sidra/get_table_sidra_use_case.py

from typing import Dict, Any, Optional
# Importamos a função de infraestrutura que faz o trabalho real
# src/domain/use_cases/sidra/get_table_sidra_use_case.py

from src.infrastructure.shared.sidra_scraper import get_structured_description

class GetTableSidrapyUseCase:
   def execute(self, table_id: int) -> Optional[Dict[str, Any]]:

 
 # Delega a requisição HTTP e o parsing para a função de infraestrutura.
        structured_data = get_structured_description(table_id)
 
        if structured_data:
            print(f"Metadados da tabela {table_id} obtidos e estruturados com sucesso.")
 
 # A função get_structured_description já trata os erros e retorna None
        return structured_data