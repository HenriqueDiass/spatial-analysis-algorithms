# src/infrastructure/controllers/pysus/cnes/routes.py

from fastapi import APIRouter, Query
from typing import List, Optional


from .get_variables_cnes_controller import get_variables_cnes_controller
from .fetch_data_cnes_controller import fetch_cnes_data_controller

# Define um único roteador para todas as rotas de CNES
cnes_router = APIRouter()

# --- Rota 1: Listar Variáveis Disponíveis ---
@cnes_router.get(
    "/variables",
    tags=["PySUS - CNES"],
    summary="Lista as variáveis (grupos) disponíveis para o CNES",
    description="Busca a lista de grupos de dados disponíveis no Cadastro Nacional de Estabelecimentos de Saúde."
)
def get_cnes_variables_route():

    return get_variables_cnes_controller()


# --- Rota 2: Buscar Dados Completos ---
@cnes_router.get(
    "/fetch-data",
    tags=["PySUS - CNES"], 
    summary="Busca e baixa dados completos do sistema CNES"
)
def get_cnes_data_route(
    group_code: str = Query(..., description="Código do grupo de dados. Ex: 'ST' para estabelecimentos.", example="ST"),
    years: List[int] = Query(..., description="Lista de anos para a consulta. Ex: 2022,2023", example=[2023]),
    states: Optional[List[str]] = Query(None, description="Lista opcional de siglas de estados (UFs) para filtrar. Ex: PE,SP", example=["PE", "SP"])
):

    return fetch_cnes_data_controller(
        group_code=group_code, 
        years=years, 
        states=states
    )