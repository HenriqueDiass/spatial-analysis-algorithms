# src/domain/use-cases/ibge/regions_intermediate/fetch-data-intermediate-regions.use-case.py
"""
Use case to fetch geometry data for all Intermediate Regions in Brazil.
"""
from typing import List, Dict, Any, Optional
import time
from backend.src.infrastructure.shared import ibge_client

# Constants to improve readability and maintainability.
IBGE_REGION_TYPE_INTERMEDIATE = "regioes-intermediarias"
API_REQUEST_DELAY_SECONDS = 0.1

class FetchDataIntermediateRegionsUseCase:
    """
    Orchestrates fetching data from the IBGE API for all Intermediate Regions
    across all states of Brazil.
    """
    def execute(self) -> Optional[List[Dict[str, Any]]]:
        """
        Executes the use case.

        Returns:
            A list of GeoJSON features with the data for all intermediate regions,
            or None if the initial search for states fails.
        """
        # Step 1: Fetch the list of all Brazilian states to iterate through them.
        states_dataframe = ibge_client.fetch_states()
        if states_dataframe is None:
            # Cannot proceed if the list of states is unavailable.
            return None

        # This list will store the final GeoJSON feature for each region.
        geojson_features_list = []

        # Step 2: Loop through each state to find its intermediate regions.
        for _, state_row in states_dataframe.iterrows():
            state_id = state_row['id']
            state_abbreviation = state_row['abbreviation']

            # Step 3: For the current state, fetch its list of intermediate regions.
            regions_dataframe = ibge_client.fetch_regions_by_state(state_id, IBGE_REGION_TYPE_INTERMEDIATE)
            if regions_dataframe is None:
                # Skip this state if it has no regions or if there was an API error.
                continue

            # Step 4: Loop through each region found in the current state.
            for _, region_row in regions_dataframe.iterrows():
                region_id = region_row['id']
                region_name = region_row['name']

                # Step 5: Fetch the geometric mesh (the polygon) for this specific region.
                geographic_mesh = ibge_client.fetch_geojson_mesh(IBGE_REGION_TYPE_INTERMEDIATE, region_id)

                # Add a respectful delay to avoid overwhelming the IBGE API.
                time.sleep(API_REQUEST_DELAY_SECONDS)

                # Step 6: If the mesh was found, enrich it with properties and add to our results.
                if geographic_mesh and 'features' in geographic_mesh and geographic_mesh['features']:
                    single_feature = geographic_mesh['features'][0]
                    
                    # Add useful context to the feature's properties.
                    single_feature['properties']['intermediate_region_id'] = region_id
                    single_feature['properties']['intermediate_region_name'] = region_name
                    single_feature['properties']['state_abbreviation'] = state_abbreviation
                    
                    geojson_features_list.append(single_feature)

        # Step 7: Return the complete list of enriched GeoJSON features.
        return geojson_features_list