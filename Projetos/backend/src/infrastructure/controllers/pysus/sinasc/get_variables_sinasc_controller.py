# src/infrastructure/controllers/pysus/sinasc/get_variables_sinasc_controller.py

from fastapi.responses import JSONResponse
from fastapi import status
from backend.src.domain.use_cases.pysus.sinasc.get_variables_sinasc_use_case import GetVariablesSinascUseCase

def get_variables_sinasc_controller():
    """
    Controller para lidar com a requisição das variáveis (grupos) do SINASC.
    """
    try:
        use_case = GetVariablesSinascUseCase()
        sinasc_groups = use_case.execute()

        if sinasc_groups is not None:
            response_data = {
                "informationSystem": "SINASC",
                "description": "Sistema de Informações sobre Nascidos Vivos",
                "variables": sinasc_groups
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Não foi possível encontrar as variáveis do SINASC na fonte de dados."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro de servidor ao buscar variáveis do SINASC: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )