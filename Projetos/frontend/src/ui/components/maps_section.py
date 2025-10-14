# src/ui/components/maps_section.py

import streamlit as st
from io import BytesIO
from src.services.api_services import fetch_birthrate_map # Renamed function

from src.ui.constants import METRIC_OPTIONS

def display_map_generation_section():
    """ SECTION 3: Map Generation. """
    st.divider()
    st.header("3. Generate Birth Rate Map by State")

    with st.container():
        col_map_1, col_map_2 = st.columns(2)

        with col_map_1:
            state_abbr_map = st.text_input(
                "State Abbreviation (UF)",
                value="PE",
                max_chars=2,
                help="Ex: PE, SP, BA."
            ).upper()

        with col_map_2:
            year_map = st.number_input(
                "Analysis Year (SINASC/Population)",
                min_value=2010,
                max_value=2024,
                value=2022,
                step=1
            )

        metric_label_map = st.selectbox(
            "Metric to Map",
            options=list(METRIC_OPTIONS.keys())
        )

        map_submitted = st.button("Generate Choropleth Map")

    if map_submitted and state_abbr_map and len(state_abbr_map) == 2:
        metric_column_name = METRIC_OPTIONS[metric_label_map]

        with st.spinner(f"Generating choropleth map for {metric_label_map} in {state_abbr_map} for {year_map}..."):
            map_content = fetch_birthrate_map( # Renamed function call
                state_abbr=state_abbr_map,
                year=year_map,
                metric_column=metric_column_name
            )

            if map_content:
                st.success("✅ Map generated successfully!")
                st.image(
                    BytesIO(map_content),
                    caption=f"Map: {metric_label_map} in {state_abbr_map}/{year_map}",
                    use_container_width=True
                )