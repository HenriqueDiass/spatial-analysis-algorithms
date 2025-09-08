# discovery/inspectors/sinan_inspector.py

import json
from pysus import SINAN
from typing import Dict, Any, Optional

def get_sinan_parameters() -> Optional[Dict[str, Any]]:
    """
    Exibe as doenças do SINAN em formato JSON, coleta os parâmetros do usuário,
    valida os dados e os retorna em um dicionário.
    """
    print("--- 🔬 Coleta de Parâmetros para o SINAN ---")
    try:
        sinan = SINAN().load()
        
        if not sinan.diseases:
            print("  Não foi possível carregar a lista de doenças.")
            return None
        
        # --- INÍCIO DA MODIFICAÇÃO: Exibição em formato JSON ---
        print("\n📋 Doenças (agravos) disponíveis no SINAN:")
        
        conditions_list = [
            {"code": code, "name": name} for code, name in sinan.diseases.items()
        ]
        
        diseases_json = {
            "informationSystem": "SINAN",
            "description": "Sistema de Informação de Agravos de Notificação",
            "conditions": conditions_list
        }
        
        # Imprime o JSON formatado
        print(json.dumps(diseases_json, indent=2, ensure_ascii=False))
        # --- FIM DA MODIFICAÇÃO ---
            
        print("\nℹ️  Preencha os parâmetros abaixo para iniciar a busca.")
        
        # --- Coleta as entradas do usuário (esta parte não muda) ---
        disease_code = input("\nDigite o código da doença (ex: DENG, ZIKA, CHIK): ").strip().upper()
        years_input_str = input("Digite o(s) ano(s), separados por vírgula (ex: 2024,2025): ").strip()
        state_abbr_input = input("Digite a sigla de UM estado para filtrar (ou deixe em branco para todos): ").strip().upper()

        # --- Valida as entradas (esta parte não muda) ---
        if disease_code not in sinan.diseases:
            print(f"❌ Código da doença '{disease_code}' inválido!")
            return None
        
        if not years_input_str:
            print("❌ O campo de ano(s) é obrigatório.")
            return None

        try:
            years = [int(y.strip()) for y in years_input_str.split(",")]
        except ValueError:
            print("❌ Formato de ano inválido! Use apenas números separados por vírgula.")
            return None

        state = state_abbr_input if state_abbr_input and len(state_abbr_input) == 2 else None

        print("------------------------------------------")
        # Retorna um dicionário com os parâmetros validados
        return {
            "disease_code": disease_code,
            "years": years,
            "state": state
        }

    except Exception as e:
        print(f"❌ Erro ao buscar opções do SINAN: {e}")
        return None