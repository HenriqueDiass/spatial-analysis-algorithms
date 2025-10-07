from fastapi import APIRouter, Query
# Importa dos controllers
from .fetch_tables_sidra_controller import fetch_all_tables_controller
from .get_table_sidra_controller import get_single_table_controller
from .fetch_specific_table_sidra_controller import fetch_specific_table_controller


sidra_router = APIRouter()

# 1. Rota Estática de Consulta Específica (PRIORIDADE: EVITAR CONFLITO DE ROTA)
@sidra_router.get(
    "/tables/fetch-specific",
    tags=["IBGE - Sidra"],
    summary="Consulta dados de uma tabela específica do SIDRA com parâmetros"
)
def fetch_specific_table_route(
    table_code: str = Query(..., description="Código da tabela SIDRA"),
    territorial_level: str = Query(..., description="Nível territorial (ex: '1' para Brasil, '6' para Município)"),
    # ATENÇÃO: A descrição foi atualizada para guiar o usuário na busca por estado/município
    ibge_territorial_code: str = Query("all", description="Código IBGE do território (ex: '31' para MG ou 'all')"),
    variable: str = Query(None, description="Código da variável (opcional)"),
    classification: str = Query(None, description="Código da classificação (opcional)"),
    categories: str = Query(None, description="Código das categorias (opcional)"),
    period: str = Query("all", description="Período da consulta (ex: '2022', '2010-2020')"),
):
    """
    Endpoint que consulta dados de uma tabela específica do SIDRA usando os parâmetros informados.
    """
    params = {
        "table_code": table_code,
        "territorial_level": territorial_level,
        "ibge_territorial_code": ibge_territorial_code,
        "variable": variable,
        "classification": classification,
        "categories": categories,
        "period": period,
    }

    # LÓGICA DE CORREÇÃO PARA MUNICÍPIOS DE UM ESTADO
    # Se o nível é Município (6) E o código não é 'all' (o usuário passou um código de estado, ex: "31")
    #if params["territorial_level"] == "6" and params["ibge_territorial_code"] != "all":
     #   codigo_estado = params["ibge_territorial_code"]
        
        
     #   params["ibge_territorial_code"] = f"all in n3 {codigo_estado}"
 

    # Remove parâmetros nulos (mantendo a remoção de nulos no final)
    params = {k: v for k, v in params.items() if v is not None}

    return fetch_specific_table_controller(params)


# 2. Rota Dinâmica (Vem em segundo para evitar o erro 422)
@sidra_router.get(
    "/tables/{table_id}",
    tags=["IBGE - Sidra"],
    summary="Busca os metadados de uma tabela específica do Sidra"
)
def get_sidra_table_metadata_route(table_id: int):
    return get_single_table_controller(table_id=table_id)


# 3. Rota Estática /tables
@sidra_router.get(
    "/tables",
    tags=["IBGE - Sidra"],
    summary="Lista todas as pesquisas e tabelas disponíveis no Sidra"
)
def get_all_sidra_tables_route():
    return fetch_all_tables_controller()