# src/infrastructure/controllers/ibge/regions_immediate/fetch-data-immediate-regions.controller.py
from fastapi import HTTPException
from backend.src.domain.use_cases.ibge.regions_intermediate import FetchDataImmediateRegionsUseCase

def fetch_all_immediate_regions():
    """
    Controller to handle the request for fetching data for all immediate regions in Brazil.
    """
    try:
        use_case = FetchDataImmediateRegionsUseCase()
        regions_features = use_case.execute()

        if regions_features is None:
            raise HTTPException(status_code=503, detail="Could not fetch immediate regions data from the external service.")

        return {
            "type": "FeatureCollection",
            "features": regions_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")