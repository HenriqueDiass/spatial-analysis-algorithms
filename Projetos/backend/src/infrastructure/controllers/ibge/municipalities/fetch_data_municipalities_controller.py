# src/infrastructure/controllers/ibge/municipalities/fetch-data-municipalities.controller.py
from fastapi import HTTPException
from backend.src.domain.use_cases.ibge.municipalities import FetchDataMunicipalitiesUseCase

def fetch_municipalities_by_state(state_abbr: str):
    """
    Controller to handle the request for fetching data for municipalities of a specific state.
    """
    try:
        use_case = FetchDataMunicipalitiesUseCase()
        municipalities_features = use_case.execute(state_abbr=state_abbr)

        if municipalities_features is None:
            # This error suggests the state abbreviation was invalid or had no data.
            raise HTTPException(status_code=404, detail=f"No data found for state '{state_abbr.upper()}'. Please provide a valid state abbreviation.")

        return {
            "type": "FeatureCollection",
            "features": municipalities_features
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")