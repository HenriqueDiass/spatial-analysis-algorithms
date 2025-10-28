# src/infrastructure/controllers/pysus/cnes/get_variables_cnes_controller.py

from fastapi.responses import JSONResponse
from fastapi import status

from backend.src.domain.use_cases.pysus.cnes.get_variables_cnes_use_case import GetVariablesCnesUseCase

def get_variables_cnes_controller():
 
    try:
        use_case = GetVariablesCnesUseCase()
        cnes_groups = use_case.execute()

        if cnes_groups is not None:
            response_data = {
                "informationSystem": "CNES",
                "description": "Cadastro Nacional de Estabelecimentos de Saúde",
                "variables": cnes_groups
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Não foi possível encontrar as variáveis do CNES na fonte de dados."},
                status_code=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        print(f"Erro de servidor ao buscar variáveis do CNES: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )