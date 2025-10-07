# src/infrastructure/controllers/pysus/sih/routes.py

from fastapi import APIRouter, Query
from typing import List, Optional

# Importa os DOIS controllers do SIH
from .get_variables_sih_controller import get_variables_sih_controller
from .fetch_data_sih_controller import fetch_sih_data_controller

# Define um único roteador para todas as rotas do SIH
sih_router = APIRouter()

# --- Rota 1: Listar Variáveis Disponíveis ---
@sih_router.get(
    "/variables",
    tags=["PySUS - SIH"],
    summary="Lista as variáveis (grupos) disponíveis para o SIH"
)
def get_sih_variables_route():
    """Endpoint para obter as variáveis (grupos) disponíveis do SIH."""
    return get_variables_sih_controller()


# --- Rota 2: Buscar Dados Completos ---
@sih_router.get(
    "/fetch-data",
    tags=["PySUS - SIH"],
    summary="Busca e baixa dados completos do sistema SIH"
)
def get_sih_data_route(
    group_code: str = Query(..., description="Código do grupo de dados. Ex: 'RD' para Autorização de Internação Hospitalar.", example="RD"),
    years: List[int] = Query(..., description="Lista de anos para a consulta. Ex: 2022,2023", example=[2023]),
    states: Optional[List[str]] = Query(None, description="Lista opcional de siglas de estados (UFs) para filtrar. Ex: PE,SP", example=["PE"]),
    months: Optional[List[int]] = Query(None, description="Lista opcional de meses para filtrar. Ex: 1,2,3 para Jan/Fev/Mar", example=[10, 11])
):
    """
    Endpoint para buscar dados do SIH (Sistema de Informações Hospitalares).
    """
    # A rota apenas repassa os parâmetros recebidos para o controller
    return fetch_sih_data_controller(
        group_code=group_code,
        years=years,
        states=states,
        months=months
    )