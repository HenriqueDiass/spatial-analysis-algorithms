# src/infrastructure/controllers/pysus/sinasc/get_summary_sinasc_controller.py

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional

# Importe o UseCase correspondente
from backend.src.domain.use_cases.pysus.sinasc.get_summary_sinasc_use_case import GetSummarySinascUseCase

# Garanta que o nome da função está correto
def get_sinasc_summary_controller(group_code: str, years: List[int], states: Optional[List[str]]):
    """
    Controller para buscar o sumário agregado de nascimentos do SINASC.
    """
    try:
        if not years:
            raise HTTPException(status_code=400, detail="O parâmetro 'years' é obrigatório.")

        params = {
            "group_code": group_code.upper(),
            "years": years,
            "states": [st.upper() for st in states] if states else None
        }

        use_case = GetSummarySinascUseCase()
        # O caso de uso já retorna o dicionário pronto
        summary_dict = use_case.execute(**params)

        if summary_dict: # Verifica se o dicionário não está vazio
            return JSONResponse(
                content=summary_dict,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"message": "Nenhum dado encontrado para os parâmetros fornecidos."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro interno ao buscar sumário do SINASC: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )