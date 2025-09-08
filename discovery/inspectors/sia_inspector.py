# discovery/inspectors/sia_inspector.py

import json
from pysus.ftp.databases import SIA
from typing import Dict, Any, Optional

def get_sia_parameters() -> Optional[Dict[str, Any]]:
    """
    Exibe os grupos do SIA em formato JSON, coleta os parâmetros do usuário de forma interativa,
    valida os dados e os retorna em um dicionário.
    """
    print("--- 🔬 Coleta de Parâmetros para o SIA ---")
    try:
        sia = SIA().load()
        
        if not sia.groups:
            print("  Não foi possível carregar os grupos.")
            return None
        
        # --- Exibição em formato JSON ---
        print("\n📋 Grupos de dados disponíveis no SIA:")

        groups_list = [
            {"code": code, "name": description} for code, description in sia.groups.items()
        ]

        groups_json = {
            "informationSystem": "SIA",
            "description": "Sistema de Informações Ambulatoriais",
            "groups": groups_list
        }
        
        print(json.dumps(groups_json, indent=2, ensure_ascii=False))
        # --- Fim da Exibição ---
            
        print("\nℹ️  Preencha os parâmetros abaixo para iniciar a busca.")

        # --- Coleta as entradas do usuário ---
        group_code = input("\nDigite o código do grupo (ex: PA): ").strip().upper()
        years_input = input("Digite o(s) ano(s), separados por vírgula: ").strip()
        states_input = input("Digite a(s) sigla(s) do(s) estado(s), separadas por vírgula (ou deixe em branco para todos): ").upper().strip()
        months_input = input("Digite o(s) mês(es), separados por vírgula (ou deixe em branco): ").strip()

        # --- Valida as entradas ---
        if group_code not in sia.groups:
            print(f"❌ Código de grupo '{group_code}' inválido!")
            return None
        
        if not years_input:
            print("❌ O campo de ano(s) é obrigatório.")
            return None

        try:
            years = [int(y.strip()) for y in years_input.split(',')]
            months = [int(m.strip()) for m in months_input.split(',')] if months_input else None
        except ValueError:
            print("❌ Formato de ano ou mês inválido! Use apenas números separados por vírgula.")
            return None

        states = [s.strip() for s in states_input.split(',')] if states_input else None
        
        print("------------------------------------------")
        # Retorna um dicionário com os parâmetros validados
        return {
            "group_code": group_code,
            "years": years,
            "states": states,
            "months": months
        }

    except Exception as e:
        print(f"❌ Erro ao buscar opções do SIA: {e}")
        return None