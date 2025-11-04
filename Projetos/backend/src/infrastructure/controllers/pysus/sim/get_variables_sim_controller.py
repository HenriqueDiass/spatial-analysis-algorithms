# src/infrastructure/controllers/pysus/sim/get_variables_sim_controller.py

from fastapi.responses import JSONResponse
from fastapi import status
from src.domain.use_cases.pysus.sim.get_variables_sim_use_case import GetVariablesSimUseCase

def get_variables_sim_controller():
    """
    Controller para lidar com a requisição das variáveis (grupos) do SIM.
    """
    try:
        use_case = GetVariablesSimUseCase()
        sim_groups = use_case.execute()

        if sim_groups is not None:
            response_data = {
                "informationSystem": "SIM",
                "description": "Sistema de Informações sobre Mortalidade",
                "variables": sim_groups
            }
            return JSONResponse(
                content=response_data,
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"error": "Não foi possível encontrar as variáveis do SIM na fonte de dados."},
                status_code=status.HTTP_404_NOT_FOUND
            )

    except Exception as e:
        print(f"Erro de servidor ao buscar variáveis do SIM: {e}")
        return JSONResponse(
            content={"error": "Ocorreu um erro interno no servidor."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )