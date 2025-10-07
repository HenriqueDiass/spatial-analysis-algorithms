# src/infrastructure/controllers/ibge/municipalities/routes.py
from fastapi import APIRouter
from . import fetch_data_municipalities

router = APIRouter()

@router.get("/{state_abbr}/fetch-data", summary="Busca dados dos municípios de um estado")
def get_municipalities_by_state_route(state_abbr: str):
    return fetch_data_municipalities.fetch_municipalities_by_state(state_abbr)