# src/infrastructure/controllers/pysus/systems/get_available_systems_controller.py

from fastapi.responses import JSONResponse
from fastapi import status

# --- CORREÇÃO ESTÁ NESSA LINHA ---
# A importação começa com 'src' e aponta para o arquivo .py específico.
from src.domain.use_cases.pysus.systems.get_available_systems_use_case import GetAvailablePysusSystemsUseCase

def get_available_pysus_systems_controller():
    """
    Controller para lidar com a requisição que lista os sistemas PySUS disponíveis.
    """
    try:
        use_case = GetAvailablePysusSystemsUseCase()
        available_systems = use_case.execute()

        return JSONResponse(
            content=available_systems,
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        print(f"Erro de servidor ao listar sistemas PySUS: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno ao buscar la lista de sistemas."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )