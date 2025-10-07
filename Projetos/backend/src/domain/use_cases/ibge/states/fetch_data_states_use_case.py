# src/domain/use-cases/ibge/states/fetch-data-states.use-case.py
"""
Use case to fetch detailed data (geometry, population) for all Brazilian states.
"""
from typing import List, Dict, Any, Optional
import time
from src.infrastructure.shared import ibge_client

# Constants for IBGE API parameters to make the code self-documenting.
IBGE_TERRITORIAL_LEVEL_STATE = "N3"
IBGE_LOCALITY_TYPE_STATES = "estados"
API_REQUEST_DELAY_SECONDS = 0.1

class FetchDataStatesUseCase:
    """
    Orchestrates fetching detailed data for every state in Brazil,
    including their geometric mesh and population.
    """
    def execute(self) -> Optional[List[Dict[str, Any]]]:
        """
        Executes the use case.

        Returns:
            A list of GeoJSON features, each representing a state with its data,
            or None if the initial search for states fails.
        """
        # Step 1: Fetch the basic list of all Brazilian states.
        states_dataframe = ibge_client.fetch_states()
        if states_dataframe is None:
            # If we can't get the list of states, we cannot proceed.
            return None

        # This list will store the final, enriched GeoJSON feature for each state.
        geojson_features_list = []

        # Step 2: Loop through each state in the DataFrame to fetch its details.
        for _, state_row in states_dataframe.iterrows():
            # Extract basic info for the current state.
            state_id = state_row['id']
            state_abbreviation = state_row['abbreviation']
            state_name = state_row['name']

            # Step 3: Fetch the specific geometric mesh (polygon) and population for this state.
            geographic_mesh = ibge_client.fetch_geojson_mesh(IBGE_LOCALITY_TYPE_STATES, state_id)
            population_count = ibge_client.fetch_population(IBGE_TERRITORIAL_LEVEL_STATE, state_id)

            # Add a small delay to be respectful to the IBGE API.
            time.sleep(API_REQUEST_DELAY_SECONDS)

            # Step 4: If the mesh was successfully retrieved, enrich it with all collected data.
            if geographic_mesh and 'features' in geographic_mesh and geographic_mesh['features']:
                single_feature = geographic_mesh['features'][0]
                
                # Add all relevant data to the GeoJSON 'properties'.
                single_feature['properties']['abbreviation'] = state_abbreviation
                single_feature['properties']['name'] = state_name
                single_feature['properties']['population_2021'] = population_count
                
                geojson_features_list.append(single_feature)

        # Step 5: Return the complete list of enriched GeoJSON features.
        return geojson_features_list