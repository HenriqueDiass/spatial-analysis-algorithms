# use_cases/discovery/list_brazilian_states.py
"""
Use case to list all Brazilian states by fetching them directly from
the official IBGE source via the 'geobr' library.
"""
import geobr
from shared.display_utils import print_formatted_list

def execute() -> None:
    print("\nBuscando dados oficiais de todos os estados do Brasil via geobr...")
    print("Aviso: Isso pode levar um momento na primeira execução.")

    try:
        # geobr.read_state() baixa os dados mais recentes de todos os estados
        gdf_states = geobr.read_state()

        formatted_items = []
        for _, row in gdf_states.sort_values(by='name_state').iterrows():
            print(row)
            # --- ALTERAÇÃO AQUI ---
            # Adicionado int() para converter o código do estado para inteiro
            line = f"Nome: {row['name_state']} | Sigla: {row['abbrev_state']} | Código IBGE: {int(row['code_state'])}"
            states = { "name_state": row['name_state'], "abbrev_state": row['abbrev_state'], "code_state": row['code_state']}
            
            formatted_items.append(states)

        print("Estados Brasileiros (Fonte: IBGE via geobr)")
        print(formatted_items)
        # print_formatted_list(
        #     title="Estados Brasileiros (Fonte: IBGE via geobr)",
        #     items=formatted_items
        # )

    except Exception as e:
        print(f"\nERRO: Falha ao baixar ou processar os dados dos estados.")
        print(f"Verifique sua conexão com a internet e se a biblioteca 'geobr' está instalada corretamente.")
        print(f"Detalhes: {e}")