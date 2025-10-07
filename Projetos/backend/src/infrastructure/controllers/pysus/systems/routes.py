# src/infrastructure/controllers/pysus/systems/routes.py

from fastapi import APIRouter
# O import do controller agora usa '.' porque está na mesma pasta
from .get_available_systems_controller import get_available_pysus_systems_controller

# Vamos dar um nome específico para este roteador para ficar claro
systems_router = APIRouter()

@systems_router.get(
    "/",  # A rota agora é a raiz, pois o prefixo será '/pysus/systems'
    tags=["PySUS"],
    summary="Lista todos os sistemas PySUS suportados pela API"
)
def get_pysus_systems_route():
    """
    Endpoint para obter a lista de todos os sistemas PySUS disponíveis.
    """
    return get_available_pysus_systems_controller()