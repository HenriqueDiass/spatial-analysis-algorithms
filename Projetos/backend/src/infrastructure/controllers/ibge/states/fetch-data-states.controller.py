# src/infrastructure/controllers/ibge/states/fetch-data-states.controller.py
from fastapi import HTTPException
from src.domain.use_cases.ibge.states import FetchDataStatesUseCase

def fetch_all_states_data():
    """
    Controller to handle the request for fetching detailed data for all states.
    """
    try:
        use_case = FetchDataStatesUseCase()
        states_features = use_case.execute()

        if states_features is None:
            # This error suggests the IBGE service might be down or unresponsive.
            raise HTTPException(status_code=503, detail="Could not fetch state list from the external service.")
        
        # Formats the list of features into a valid GeoJSON FeatureCollection.
        return {
            "type": "FeatureCollection",
            "features": states_features
        }

    except Exception as e:
        # Generic error handler for any unexpected issues.
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")