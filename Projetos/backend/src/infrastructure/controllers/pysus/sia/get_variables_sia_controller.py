# src/infrastructure/controllers/pysus/sia/get_variables_sia_controller.py

from fastapi.responses import JSONResponse
from fastapi import status
from src.domain.use_cases.pysus.sia.get_variables_sia_use_case import GetVariablesSiaUseCase

def get_variables_sia_controller():
    
    try:
        use_case = GetVariablesSiaUseCase()
        sia_groups = use_case.execute()

        if sia_groups is not None:
            response_data = {
                "informationSystem": "SIA",
                "description": "Sistema de Informações Ambulatoriais",
                "variables": sia_groups
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Não foi possível encontrar as variáveis do SIA na fonte de dados."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro de servidor ao buscar variáveis do SIA: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )