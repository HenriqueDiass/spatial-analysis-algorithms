# src/infrastructure/controllers/ibge/regions_intermediate/fetch-data-intermediate-regions.controller.py
from fastapi import HTTPException
from src.domain.use_cases.ibge.regions_intermediate import FetchDataIntermediateRegionsUseCase

def fetch_all_intermediate_regions():
    """
    Controller to handle the request for fetching data for all intermediate regions in Brazil.
    """
    try:
        use_case = FetchDataIntermediateRegionsUseCase()
        regions_features = use_case.execute()

        if regions_features is None:
            raise HTTPException(status_code=503, detail="Could not fetch intermediate regions data from the external service.")

        return {
            "type": "FeatureCollection",
            "features": regions_features
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")