# src/infrastructure/controllers/maps/routes.py

from fastapi import APIRouter, Query
from enum import Enum

from .get_map_birthrate_controller import generate_birth_rate_map

class BirthRateMetric(str, Enum):
    total_births = "total_births"
    birth_rate_per_1000 = "birth_rate_per_1000"
    births_mother_under20 = "births_mother_under20"
    births_mother_20to29 = "births_mother_20to29"
    births_mother_30to39 = "births_mother_30to39"
    births_mother_40plus = "births_mother_40plus"

maps_router = APIRouter()

@maps_router.get(
    "/{state_abbr}/{year}/birth-rate", 
    tags=["Mapas"],
    summary="Gera um mapa coroplético de natalidade para um estado e ano"
)
def get_map_birthrate_route(
    state_abbr: str, 
    year: int,
    # --- NOVO PARÂMETRO ADICIONADO AQUI ---
    group_code: str = Query(
        default="DN", 
        description="Código do grupo de dados do SINASC (ex: 'DN' para Declaração de Nascido Vivo).",
        example="DN"
    ),
    # ----------------------------------------
    metric: BirthRateMetric = Query(
        default=BirthRateMetric.birth_rate_per_1000,
        description="A métrica de natalidade a ser exibida no mapa."
    )
):
    """
    Gera e retorna uma imagem PNG de um mapa de coropletas sobre nascimentos.
    """
    # Passamos o novo parâmetro para o controller
    return generate_birth_rate_map(
        state_abbr=state_abbr, 
        year=year, 
        metric=metric.value,
        group_code=group_code # <-- MUDANÇA
    )