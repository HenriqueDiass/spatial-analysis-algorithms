# use_cases/discovery/listers/list_geobr_datasets.py
import geobr
from shared.display_utils import print_formatted_list

def execute() -> None:
    """Fetches and displays all available datasets from the geobr library."""
    print("Fetching available datasets from geobr library...")
    try:
        datasets_df = geobr.list_geobr()
        formatted_items = [
            f"{row['geography'].capitalize()} (Function: geobr.read_{row['function']}())"
            for _, row in datasets_df.iterrows()
        ]
        print_formatted_list("Datasets Available in GeoBR", formatted_items)
    except Exception as e:
        print(f"ERROR: Could not fetch from geobr. Details: {e}")