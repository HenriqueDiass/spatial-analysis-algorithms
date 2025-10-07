# src/infrastructure/controllers/pysus/sinasc/routes.py

from fastapi import APIRouter, Query
from typing import List, Optional

# Importa os DOIS controllers do SINASC
from .get_variables_sinasc_controller import get_variables_sinasc_controller
from .get_summary_sinasc_controller import get_sinasc_summary_controller

# Define um único roteador para todas as rotas do SINASC
sinasc_router = APIRouter()

# --- Rota 1: Listar Variáveis Disponíveis ---
@sinasc_router.get(
    "/variables",
    tags=["PySUS - SINASC"],
    summary="Lista as variáveis (grupos) disponíveis para o SINASC"
)
def get_sinasc_variables_route():
    """Endpoint para obter as variáveis (grupos) disponíveis do SINASC."""
    return get_variables_sinasc_controller()


# --- Rota 2: Obter Sumário Agregado ---
@sinasc_router.get(
    "/get-summary",
    tags=["PySUS - SINASC"],
    summary="Busca dados do SINASC e retorna um sumário agregado de nascimentos"
)
def get_sinasc_summary_route(
    group_code: str = Query(..., description="Código do grupo de dados. Ex: 'DN' para Declaração de Nascido Vivo.", example="DN"),
    years: List[int] = Query(..., description="Lista de anos para a consulta. Ex: 2021,2022", example=[2022]),
    states: Optional[List[str]] = Query(None, description="Lista opcional de siglas de estados (UFs) para filtrar. Ex: PE,SP", example=["PE"])
):
    """
    Endpoint para buscar um sumário agregado de dados do SINASC.
    """
    # A rota apenas repassa os parâmetros recebidos para o controller
    return get_sinasc_summary_controller(
        group_code=group_code,
        years=years,
        states=states
    )