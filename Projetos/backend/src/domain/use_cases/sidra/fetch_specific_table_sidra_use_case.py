import sidrapy
import pandas as pd
from typing import Dict, Any, Optional, List


class FetchSpecificTableSidraUseCase:

    def execute(self, request_params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        try:
            # Fetches data from SIDRA API using request_params
            raw_data_df = sidrapy.get_table(**request_params, header="y")

            if raw_data_df is None or raw_data_df.empty or len(raw_data_df) < 2:
                return None

            raw_data_df.columns = raw_data_df.iloc[0]
            processed_data_df = raw_data_df.drop(0).reset_index(drop=True)

            expected_column_mappings = {
                'Município (Código)': 'Municipality_ID', 'Município': 'Municipality_Name',
                'Unidade da Federação (Código)': 'State_ID', 'Unidade da Federação': 'State_Name',
                'Valor': 'Value', 'Variável': 'Variable_Name', 'Ano': 'Year'
            }

            present_column_mappings = {
                sidra_name: standard_name
                for sidra_name, standard_name in expected_column_mappings.items()
                if sidra_name in processed_data_df.columns
            }

            if not present_column_mappings:
                return processed_data_df.to_dict(orient="records")

            selected_df = processed_data_df[list(present_column_mappings.keys())].copy()
            selected_df.rename(columns=present_column_mappings, inplace=True)

            # --- Value Type Conversion ---
            if 'Value' in selected_df.columns:
                selected_df['Value'] = pd.to_numeric(selected_df['Value'], errors='coerce')

            return selected_df.to_dict(orient="records")

        except Exception as e:
            print(f"Error consulting SIDRA data: {e}")
            return None