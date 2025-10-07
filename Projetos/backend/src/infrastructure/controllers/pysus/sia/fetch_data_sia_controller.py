# src/infrastructure/controllers/pysus/sia/fetch_data_sia_controller.py

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional
import pandas as pd

# Verifique se o import do UseCase está correto
from src.domain.use_cases.pysus.sia.fetch_data_sia_use_case import FetchDataSiaUseCase

# Verifique se o nome desta função está escrito exatamente assim
def fetch_sia_data_controller(group_code: str, years: List[int], states: Optional[List[str]], months: Optional[List[int]]):
    """
    Controller para buscar e baixar os dados completos do SIA.
    """
    try:
        if not years:
            raise HTTPException(status_code=400, detail="O parâmetro 'years' é obrigatório.")

        params = {
            "group_code": group_code.upper(),
            "years": years,
            "states": [st.upper() for st in states] if states else None,
            "months": months
        }

        use_case = FetchDataSiaUseCase()
        sia_data_df = use_case.execute(**params)

        if isinstance(sia_data_df, pd.DataFrame) and not sia_data_df.empty:
            response_data = sia_data_df.to_dict(orient='records')
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"message": "Nenhum dado encontrado para os parâmetros fornecidos."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro interno ao buscar dados do SIA: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )