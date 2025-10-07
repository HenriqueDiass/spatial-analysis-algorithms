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
    metadata: Dict[str, Any],
    summary_only: bool = False  # <-- NOVO PARÂMETRO! O padrão é False para não quebrar nada.
) -> None:
    """
    Cria e salva um arquivo JSON.
    Se summary_only for True, salva apenas metadados.
    Caso contrário, salva o dataset completo.
    """
    print(f"\n📝 Gerando a saída JSON para o sistema {system_name}...")

    output_json = {} # Dicionário que será salvo no final

    # Lógica para decidir o que colocar no JSON
    if summary_only:
        # MODO RESUMO: Gera o JSON limpo, apenas com metadados.
        print("   -> Modo: Resumo (sem dados individuais).")
        output_json = {
            "informationSystem": system_name,
            **metadata
        }
    else:
        # MODO COMPLETO (comportamento antigo)
        print(f"   -> Modo: Completo ({len(dataframe)} registros).")
        dataframe_str = dataframe.astype(str)
        output_json = {
            "informationSystem": system_name,
            **metadata,
            "totalRecords": len(dataframe),
            "columns": list(dataframe.columns),
            "data": dataframe_str.to_dict(orient="records")
        }

    # A pré-visualização e o salvamento agora usam a variável 'output_json'
    print("\n📄 Pré-visualização do JSON gerado:")
    # Para a pré-visualização, mostramos o objeto inteiro, pois já é um resumo
    print(json.dumps(output_json, indent=2, ensure_ascii=False))

    print(f"\n💾 Salvando o arquivo em: {output_filename}...")
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)
        print(f"✅ Arquivo salvo com sucesso em: {output_filename}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo JSON: {e}")