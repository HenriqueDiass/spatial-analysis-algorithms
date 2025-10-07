# src/domain/use-cases/ibge/municipalities/fetch-data-municipalities.use-case.py
"""
Use case to fetch detailed data (geometry, population)
for all municipalities of a given state.
"""
from typing import List, Dict, Any, Optional
import time
from src.infrastructure.shared import ibge_client

# Constants to avoid "magic strings" and improve readability.
IBGE_TERRITORIAL_LEVEL_MUNICIPALITY = "N6"
IBGE_LOCALITY_TYPE_MUNICIPALITIES = "municipios"
API_REQUEST_DELAY_SECONDS = 0.1

class FetchDataMunicipalitiesUseCase:
    """
    Orchestrates the data fetching from the IBGE API for all municipalities
    within a specific state.
    """
    def execute(self, state_abbreviation: str) -> Optional[List[Dict[str, Any]]]:
        """
        Executes the use case.

        Args:
            state_abbreviation: The two-letter abbreviation of the state to be processed (e.g., "PE").

        Returns:
            A list of GeoJSON features containing the data for the municipalities,
            or None if the initial search fails.
        """
        # Step 1: Fetch the list of all municipalities for the given state.
        # The result is a Pandas DataFrame with columns like 'id' and 'name'.
        municipalities_dataframe = ibge_client.fetch_municipalities_by_state(state_abbreviation.upper())
        if municipalities_dataframe is None:
            # If no municipalities are found for the state, it's impossible to proceed.
            return None

        # This list will store the final GeoJSON feature for each municipality.
        geojson_features_list = []

        # Step 2: Iterate over each municipality found to fetch its detailed data.
        for _, municipality_row in municipalities_dataframe.iterrows():
            # Extract the ID and name from the current row of the DataFrame.
            municipality_id = municipality_row['id']
            municipality_name = municipality_row['name']

            # Step 3: Fetch the specific data for this single municipality.
            # 'mesh' contains the geometric shape (the polygon).
            # 'population' contains the latest population count.
            geographic_mesh = ibge_client.fetch_geojson_mesh(IBGE_LOCALITY_TYPE_MUNICIPALITIES, municipality_id)
            population_count = ibge_client.fetch_population(IBGE_TERRITORIAL_LEVEL_MUNICIPALITY, municipality_id)

            # Add a small delay to be respectful to the IBGE API and avoid rate limiting.
            time.sleep(API_REQUEST_DELAY_SECONDS)

            # Step 4: If the geometric mesh was successfully found, enrich it with our data.
            if geographic_mesh and 'features' in geographic_mesh and geographic_mesh['features']:
                # The API returns a FeatureCollection, but we only need the first (and only) feature.
                single_feature = geographic_mesh['features'][0]
                
                # Add our collected data into the 'properties' dictionary of the GeoJSON feature.
                single_feature["properties"]["name"] = municipality_name
                single_feature["properties"]["population"] = population_count
                
                # Add the completed feature to our results list.
                geojson_features_list.append(single_feature)

        # Step 5: Return the complete list of enriched GeoJSON features.
        return geojson_features_list