from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional

from src.domain.use_cases.pysus.cnes.fetch_data_cnes_use_case import FetchDataCnesUseCase

def fetch_cnes_data_controller(group_code: str, years: List[int], states: Optional[List[str]]):
    """
    Controller para buscar um resumo de dados do CNES.
    """
    try:
        params = {
            "group_code": group_code,
            "years": years,
            "states": [st.upper() for st in states] if states else None
        }

        use_case = FetchDataCnesUseCase()
        # O UseCase agora já retorna a lista de resumo pronta
        summary_list = use_case.execute(**params)

        if summary_list:
            summary_response = {
                "metadata": {
                    "system": "CNES",
                    "parameters": params,
                    "total_records_found": sum(item['total'] for item in summary_list)
                },
                "summary_by_municipality": summary_list
            }
            return JSONResponse(content=summary_response, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os parâmetros fornecidos.")

    except Exception as e:
        print(f"Erro interno ao buscar dados do CNES: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")