# src/infrastructure/controllers/pysus/sia/routes.py

from fastapi import APIRouter, Query
from typing import List, Optional

# Importa os DOIS controllers que este roteador irá usar
from .get_variables_sia_controller import get_variables_sia_controller
from .fetch_data_sia_controller import fetch_sia_data_controller

# Define um único roteador para todas as rotas do SIA
sia_router = APIRouter()

# --- Rota 1: Listar Variáveis Disponíveis ---
@sia_router.get(
    "/variables",
    tags=["PySUS - SIA"],
    summary="Lista as variáveis (grupos) disponíveis para o SIA"
)
def get_sia_variables_route():
    return get_variables_sia_controller()

@sia_router.get(
    "/fetch-data",
    tags=["PySUS - SIA"],
    summary="Busca e baixa dados completos do sistema SIA"
)
def get_sia_data_route(
    group_code: str = Query(..., description="Código do grupo de dados. Ex: 'PA' para Produção Ambulatorial.", example="PA"),
    years: List[int] = Query(..., description="Lista de anos para a consulta. Ex: 2022,2023", example=[2023]),
    states: Optional[List[str]] = Query(None, description="Lista opcional de siglas de estados (UFs) para filtrar. Ex: PE,SP", example=["SP"]),
    months: Optional[List[int]] = Query(None, description="Lista opcional de meses para filtrar. Ex: 1,2,3 para Jan/Fev/Mar", example=[1, 2])
):
    return fetch_sia_data_controller(
        group_code=group_code,
        years=years,
        states=states,
        months=months
    )