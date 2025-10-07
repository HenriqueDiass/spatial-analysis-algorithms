# src/infrastructure/controllers/pysus/cnes/fetch_data_cnes_controller.py

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional
from src.domain.use_cases.pysus.cnes.fetch_data_cnes_use_case import FetchDataCnesUseCase


def fetch_cnes_data_controller(group_code: str, years: List[int], states: Optional[List[str]]):
    
    try:
        if not years:
            raise HTTPException(status_code=400, detail="O parâmetro 'years' é obrigatório.")

        params = {
            "group_code": group_code.upper(),
            "years": years,
            "states": [st.upper() for st in states] if states else None
        }

        use_case = FetchDataCnesUseCase()
        cnes_data = use_case.execute(**params)

        if cnes_data:
            return JSONResponse(
                content=cnes_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"message": "Nenhum dado encontrado para os parâmetros fornecidos."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Ocorreu um erro interno: {e}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )