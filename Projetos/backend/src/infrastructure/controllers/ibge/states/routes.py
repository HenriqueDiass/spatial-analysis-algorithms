# src/infrastructure/controllers/ibge/states/routes.py
from fastapi import APIRouter
from . import fetch_data_states  # Importa o controller da mesma pasta

router = APIRouter()

@router.get("/fetch-data", summary="Busca dados detalhados de todos os estados")
def get_states_data_route():
    return fetch_data_states.fetch_all_states_data()