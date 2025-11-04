# src/infrastructure/controllers/pysus/sih/get_variables_sih_controller.py

from fastapi.responses import JSONResponse
from fastapi import status
from src.domain.use_cases.pysus.sih.get_variables_sih_use_case import GetVariablesSihUseCase

def get_variables_sih_controller():
    """
    Controller para lidar com a requisição das variáveis (grupos) do SIH.
    """
    try:
        use_case = GetVariablesSihUseCase()
        sih_groups = use_case.execute()

        if sih_groups is not None:
            response_data = {
                "informationSystem": "SIH",
                "description": "Sistema de Informações Hospitalares",
                "variables": sih_groups
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Não foi possível encontrar as variáveis do SIH na fonte de dados."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro de servidor ao buscar variáveis do SIH: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )