import os
import json
import pandas as pd
from typing import Dict, Any, Tuple

# Esta função está correta, não precisa de alteração
def save_sim_output(output_dir: str, params: Dict[str, Any], data_results: Tuple[pd.DataFrame, dict]):
    df, cases_per_municipality = data_results
    # ... (resto da função)

# --- CORREÇÃO NECESSÁRIA ESTÁ AQUI ---
def save_sinasc_output(output_dir: str, params: Dict[str, Any], summary_dict: dict):
    """
    Organiza e salva a saída para o SINASC, que agora é apenas um sumário em dicionário.
    """
    # 1. Checa se o dicionário recebido está vazio
    if not summary_dict:
        print("\nNenhum dado de sumário foi retornado. O arquivo JSON não foi gerado.")
        return

    # 2. Define o nome do arquivo de saída
    states_str = "_".join(params.get('states') or ['BR'])
    years_str = "_".join(map(str, params.get('years')))
    # O nome do arquivo agora corresponde ao que o orquestrador do mapa espera
    filename = f"pysus_sinasc_summary_{params['group_code']}_{years_str}_{states_str}.json"
    full_path = os.path.join(output_dir, filename)

    # 3. Monta o objeto final que será salvo, incluindo metadados
    output_data = {
        "source": "SINASC",
        "parameters": {
            "group": params["group_code"],
            "years": params["years"],
            "states": params["states"] or "Todos"
        },
        "summary_by_municipality": summary_dict
    }
    
    # 4. Salva o dicionário diretamente em um arquivo JSON
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Sumário do SINASC salvo com sucesso em: {full_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo de sumário do SINASC: {e}")

# Adicione as outras funções de save se elas existirem no seu arquivo,
# como save_cnes_output, save_sia_output, etc.