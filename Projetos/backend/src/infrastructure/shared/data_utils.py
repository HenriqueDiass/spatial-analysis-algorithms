# src/infrastructure/shared/data_utils.py
import pandas as pd
from typing import List, Dict, Any

STATE_ABBR_TO_IBGE_CODE: Dict[str, str] = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14", "PA": "15", "AP": "16", "TO": "17",
    "MA": "21", "PI": "22", "CE": "23", "RN": "24", "PB": "25", "PE": "26", "AL": "27",
    "SE": "28", "BA": "29", "MG": "31", "ES": "32", "RJ": "33", "SP": "35",
    "PR": "41", "SC": "42", "RS": "43", "MS": "50", "MT": "51", "GO": "52", "DF": "53"
}

def get_age_group(age: Any) -> str:
    """Categorizes an age into predefined groups."""
    if pd.isna(age):
        return "Ignored"
    try:
        age_int = int(age)
        if age_int < 20: return "<20"
        if age_int <= 29: return "20-29"
        if age_int <= 39: return "30-39"
        return "40+"
    except (ValueError, TypeError):
        return "Ignored"

def filter_dataframe_by_states(dataframe: pd.DataFrame, states: List[str], municipality_code_column: str) -> pd.DataFrame:
    """Filters a DataFrame based on a list of state abbreviations."""
    if not states or municipality_code_column not in dataframe.columns:
        return dataframe
    
    ibge_codes = [STATE_ABBR_TO_IBGE_CODE.get(s.upper()) for s in states if s.upper() in STATE_ABBR_TO_IBGE_CODE]
    if not ibge_codes:
        # Retorna um DataFrame vazio se não houver códigos IBGE válidos para os estados fornecidos
        return pd.DataFrame(columns=dataframe.columns)

    # O PONTO-CHAVE: Filtra as linhas verificando se os DOIS PRIMEIROS DÍGITOS
    # do código do município (que representam o código do estado) estão na lista ibge_codes.
    mask = dataframe[municipality_code_column].astype(str).str[:2].isin(ibge_codes)
    return dataframe[mask]