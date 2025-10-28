# src/infrastructure/controllers/ibge/population/fetch-data-population.controller.py
from fastapi import HTTPException
from backend.src.domain.use_cases.ibge.population import FetchDataPopulationUseCase

def fetch_population_by_state(state_abbr: str, year: int):
    """
    Controller to handle the request for fetching population data for a state in a given year.
    """
    try:
        use_case = FetchDataPopulationUseCase()
        population_data = use_case.execute(year=year, state_abbr=state_abbr)

        if population_data is None:
            raise HTTPException(status_code=404, detail=f"Population data not found for state '{state_abbr.upper()}' in year {year}.")

        return population_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")