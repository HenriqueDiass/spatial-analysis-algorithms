import json
import pandas as pd
from typing import List, Dict, Any, Optional

# --- Constantes Compartilhadas ---
STATE_ABBR_TO_IBGE_CODE = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14", "PA": "15", "AP": "16", "TO": "17",
    "MA": "21", "PI": "22", "CE": "23", "RN": "24", "PB": "25", "PE": "26", "AL": "27",
    "SE": "28", "BA": "29", "MG": "31", "ES": "32", "RJ": "33", "SP": "35",
    "PR": "41", "SC": "42", "RS": "43", "MS": "50", "MT": "51", "GO": "52", "DF": "53"
}

# --- Funções de Processamento de Dados ---

def get_age_group(age: Any) -> str:
    """Categoriza a idade em faixas etárias pré-definidas."""
    if pd.isna(age):
        return "Ignorado"
    try:
        age = int(age)
        if age < 20: return "<20"
        if age <= 29: return "20-29"
        if age <= 39: return "30-39"
        return "40+"
    except (ValueError, TypeError):
        return "Ignorado"

def filter_dataframe_by_states(dataframe: pd.DataFrame, states: List[str], municipality_code_column: str) -> pd.DataFrame:
    """Filtra um DataFrame com base em uma lista de siglas de estados."""
    if not states or not municipality_code_column in dataframe.columns:
        return dataframe

    filtered_dfs = []
    for state_abbr in states:
        ibge_code = STATE_ABBR_TO_IBGE_CODE.get(state_abbr.upper())
        if ibge_code:
            # Garante que a coluna de código do município seja tratada como string
            df_filtered_by_state = dataframe[dataframe[municipality_code_column].astype(str).str.startswith(ibge_code)]
            filtered_dfs.append(df_filtered_by_state)
    
    if not filtered_dfs:
        print(f"⚠️ Nenhum registro encontrado para o(s) estado(s): {', '.join(states)}")
        return pd.DataFrame(columns=dataframe.columns) # Retorna DF vazio

    print(f"📊 DataFrame filtrado com {len(pd.concat(filtered_dfs, ignore_index=True))} registros para o(s) estado(s): {', '.join(states)}")
    return pd.concat(filtered_dfs, ignore_index=True)


# --- Funções de Saída (Output) ---

def save_data_to_json(
    dataframe: pd.DataFrame,
    system_name: str,
    output_filename: str,
    metadata: Dict[str, Any]
) -> None:
    """
    Cria e salva um arquivo JSON completo com os dados e metadados,
    e exibe uma amostra no console.
    """
    print("\n📝 Gerando a saída JSON com todos os registros...")

    # Garante que todos os dados no DF sejam strings para evitar erros de serialização JSON
    dataframe_str = dataframe.astype(str)

    # Objeto JSON final com todos os registros
    full_json_output = {
        "informationSystem": system_name,
        **metadata,  # Adiciona metadados específicos do sistema
        "totalRecords": len(dataframe),
        "columns": list(dataframe.columns),
        "data": dataframe_str.to_dict(orient="records")
    }

    # Objeto de amostra para exibição no console
    preview_json = {
        "informationSystem": system_name,
        **metadata,
        "totalRecords": full_json_output["totalRecords"],
        "sampleData": full_json_output["data"][:5] # Apenas os 5 primeiros para preview
    }
    
    # Adiciona dados sumarizados ao preview se existirem
    if "casesPerMunicipality" in full_json_output:
        preview_json["casesPerMunicipality_sample"] = full_json_output["casesPerMunicipality"][:5]


    print("\n📄 Pré-visualização do JSON (metadados e 5 primeiros registros):")
    print(json.dumps(preview_json, indent=2, ensure_ascii=False))

    print(f"\n💾 Salvando o dataset completo em: {output_filename}...")
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(full_json_output, f, indent=2, ensure_ascii=False)
        print(f"✅ Arquivo salvo com sucesso em: {output_filename}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo JSON: {e}")