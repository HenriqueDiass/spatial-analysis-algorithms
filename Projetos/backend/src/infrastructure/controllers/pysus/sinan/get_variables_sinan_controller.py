# src/infrastructure/controllers/pysus/sinan/get_variables_sinan_controller.py

from fastapi.responses import JSONResponse
from fastapi import status
from backend.src.domain.use_cases.pysus.sinan.get_variables_sinan_use_case import GetVariablesSinanUseCase

def get_variables_sinan_controller():
    """
    Controller para lidar com a requisição das variáveis (doenças) do SINAN.
    """
    try:
        use_case = GetVariablesSinanUseCase()
        sinan_diseases = use_case.execute()

        if sinan_diseases is not None:
            response_data = {
                "informationSystem": "SINAN",
                "description": "Sistema de Informação de Agravos de Notificação",
                "variables": sinan_diseases
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Não foi possível encontrar as variáveis do SINAN na fonte de dados."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro de servidor ao buscar variáveis do SINAN: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )