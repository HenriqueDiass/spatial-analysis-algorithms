# src/infrastructure/controllers/pysus/sinan/routes.py

from fastapi import APIRouter, Query
from typing import List, Optional

# Importa os DOIS controllers do SINAN
from .get_variables_sinan_controller import get_variables_sinan_controller
from .fetch_data_sinan_controller import fetch_sinan_data_controller

# Define um único roteador para todas as rotas do SINAN
sinan_router = APIRouter()

# --- Rota 1: Listar Variáveis Disponíveis ---
@sinan_router.get(
    "/variables",
    tags=["PySUS - SINAN"],
    summary="Lista as variáveis (doenças/agravos) disponíveis para o SINAN"
)
def get_sinan_variables_route():
    """Endpoint para obter as variáveis (doenças) disponíveis do SINAN."""
    return get_variables_sinan_controller()


# --- Rota 2: Buscar Dados Completos e Sumário ---
@sinan_router.get(
    "/fetch-data",
    tags=["PySUS - SINAN"],
    summary="Busca dados do SINAN e retorna um sumário de casos por município"
)
def get_sinan_data_route(
    disease_code: str = Query(..., description="Código do agravo (doença). Ex: 'DENG' para Dengue.", example="DENG"),
    years: List[int] = Query(..., description="Lista de anos para a consulta. Ex: 2022,2023", example=[2023]),
    states: Optional[List[str]] = Query(None, description="Lista opcional de siglas de estados (UFs) para filtrar. Ex: PE,SP", example=["PE"])
):
    """
    Endpoint para buscar dados do SINAN (Sistema de Informação de Agravos de Notificação).
    Retorna os dados completos e um sumário de casos por município.
    """
    # A rota apenas repassa os parâmetros recebidos para o controller
    return fetch_sinan_data_controller(
        disease_code=disease_code,
        years=years,
        states=states
    )