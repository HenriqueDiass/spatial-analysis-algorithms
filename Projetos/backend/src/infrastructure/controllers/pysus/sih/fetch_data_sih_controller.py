# src/infrastructure/controllers/pysus/sih/fetch_data_sih_controller.py

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional
import pandas as pd

# Verifique se o import do UseCase está correto
from src.domain.use_cases.pysus.sih.fetch_data_sih_use_case import FetchDataSihUseCase

# Verifique se o nome da função está escrito exatamente assim
def fetch_sih_data_controller(group_code: str, years: List[int], states: Optional[List[str]], months: Optional[List[int]]):
    """
    Controller para buscar e baixar os dados completos do SIH.
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

        use_case = FetchDataSihUseCase()
        sih_data_df = use_case.execute(**params)

        if isinstance(sih_data_df, pd.DataFrame) and not sih_data_df.empty:
            response_data = sih_data_df.to_dict(orient='records')
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
        print(f"Erro interno ao buscar dados do SIH: {e}")
        return JSONResponse(
            content={"error": f"Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )