# src/infrastructure/controllers/pysus/sim/fetch_data_sim_controller.py

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional
import pandas as pd

# Importe o UseCase correspondente
from src.domain.use_cases.pysus.sim.fetch_data_sim_use_case import FetchDataSimUseCase

# Garanta que o nome da função está correto
def fetch_sim_data_controller(group_code: str, years: List[int], states: Optional[List[str]]):
    """
    Controller para buscar os dados do SIM e o sumário de óbitos por município.
    """
    try:
        if not years:
            raise HTTPException(status_code=400, detail="O parâmetro 'years' é obrigatório.")

        params = {
            "group_code": group_code.upper(),
            "years": years,
            "states": [st.upper() for st in states] if states else None
        }

        use_case = FetchDataSimUseCase()
        # O caso de uso do SIM retorna uma tupla com dois valores
        sim_data_df, summary_list = use_case.execute(**params)

        if isinstance(sim_data_df, pd.DataFrame) and not sim_data_df.empty:
            # Monta a resposta com as duas chaves: 'data' e 'summary_by_municipality'
            response_data = {
                "data": sim_data_df.to_dict(orient='records'),
                "summary_by_municipality": summary_list
            }
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
        print(f"Erro interno ao buscar dados do SIM: {e}")
        return JSONResponse(
            content={"error": f"Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )