# src/infrastructure/controllers/pysus/sim/routes.py

from fastapi import APIRouter, Query
from typing import List, Optional

# Importa os DOIS controllers do SIM
from .get_variables_sim_controller import get_variables_sim_controller
from .fetch_data_sim_controller import fetch_sim_data_controller

# Define um único roteador para todas as rotas do SIM
sim_router = APIRouter()

# --- Rota 1: Listar Variáveis Disponíveis ---
@sim_router.get(
    "/variables",
    tags=["PySUS - SIM"],
    summary="Lista as variáveis (grupos) disponíveis para o SIM"
)
def get_sim_variables_route():
    """Endpoint para obter as variáveis (grupos) disponíveis do SIM."""
    return get_variables_sim_controller()


# --- Rota 2: Buscar Dados Completos e Sumário ---
@sim_router.get(
    "/fetch-data",
    tags=["PySUS - SIM"],
    summary="Busca dados do SIM e retorna um sumário de óbitos por município"
)
def get_sim_data_route(
    group_code: str = Query(..., description="Código do grupo de dados. Ex: 'DO' para Declaração de Óbito.", example="DO"),
    years: List[int] = Query(..., description="Lista de anos para a consulta. Ex: 2021,2022", example=[2022]),
    states: Optional[List[str]] = Query(None, description="Lista opcional de siglas de estados (UFs) para filtrar. Ex: PE,SP", example=["PE"])
):
    """
    Endpoint para buscar dados do SIM (Sistema de Informações sobre Mortalidade).
    Retorna os dados completos e um sumário de óbitos por município.
    """
    # A rota apenas repassa os parâmetros recebidos para o controller
    return fetch_sim_data_controller(
        group_code=group_code,
        years=years,
        states=states
    )