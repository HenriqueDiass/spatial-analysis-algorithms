# discovery/inspectors/sinasc_inspector.py

import json
from pysus import SINASC
from typing import Dict, Any, Optional

def get_sinasc_parameters() -> Optional[Dict[str, Any]]:
    """
    Exibe os grupos do SINASC em formato JSON, coleta os parâmetros do usuário de forma interativa,
    valida os dados e os retorna em um dicionário.
    """
    print("--- 🔬 Coleta de Parâmetros para o SINASC ---")
    try:
        sinasc = SINASC().load()
        
        if not sinasc.groups:
            print("  Não foi possível carregar os grupos.")
            return None
        
        # --- INÍCIO DA MODIFICAÇÃO: Exibição em formato JSON ---
        print("\n📋 Grupos de dados disponíveis no SINASC:")

        groups_list = [
            {"code": code, "name": description} for code, description in sinasc.groups.items()
        ]

        groups_json = {
            "informationSystem": "SINASC",
            "description": "Sistema de Informações sobre Nascidos Vivos",
            "groups": groups_list
        }
        
        # Imprime o JSON formatado
        print(json.dumps(groups_json, indent=2, ensure_ascii=False))
        # --- FIM DA MODIFICAÇÃO ---
            
        print("\nℹ️  Preencha os parâmetros abaixo para iniciar a busca.")

        # --- Coleta as entradas do usuário (esta parte não muda) ---
        group_code = input("\nDigite o código do grupo (ex: DN): ").strip().upper()
        years_input = input("Digite o(s) ano(s), separados por vírgula: ").strip()
        states_input = input("Digite a(s) sigla(s) do(s) estado(s) para filtrar, separadas por vírgula (ou deixe em branco): ").upper().strip()

        # --- Valida as entradas (esta parte não muda) ---
        if group_code not in sinasc.groups:
            print(f"❌ Código de grupo '{group_code}' inválido!")
            return None
        
        if not years_input:
            print("❌ O campo de ano(s) é obrigatório.")
            return None

        try:
            years = [int(y.strip()) for y in years_input.split(',')]
        except ValueError:
            print("❌ Formato de ano inválido! Use apenas números separados por vírgula.")
            return None

        states = [s.strip() for s in states_input.split(',')] if states_input else None
        
        print("------------------------------------------")
        # Retorna um dicionário com os parâmetros validados
        return {
            "group_code": group_code,
            "years": years,
            "states": states
        }

    except Exception as e:
        print(f"❌ Erro ao buscar opções do SINASC: {e}")
        return None