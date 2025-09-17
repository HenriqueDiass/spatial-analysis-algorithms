import json
import os
from typing import Dict, Any, Optional

# Importa a função do nosso módulo compartilhado que busca e processa os dados
from shared.sidra_client import get_structured_description

def execute(table_id: int, output_dir: str) -> Optional[Dict[str, Any]]:
    """
    Executa o caso de uso de inspeção de uma tabela do SIDRA.

    Esta função busca os metadados da tabela, salva em um arquivo JSON
    dentro do diretório especificado em 'output_dir' e retorna os dados estruturados.

    Args:
        table_id (int): O número da tabela do SIDRA a ser inspecionada.
        output_dir (str): O caminho para o diretório onde o arquivo JSON será salvo.

    Returns:
        Um dicionário com os metadados da tabela, ou None se ocorrer um erro.
    """
    print(f"\n--- INICIANDO INSPEÇÃO DA TABELA {table_id} ---")
    
    # 1. Usa o cliente para buscar os dados
    data = get_structured_description(table_id)

    # 2. Se os dados foram obtidos com sucesso, processa e salva
    if data:
        # Cria o nome base do arquivo
        base_filename = f"tabela_{table_id}_estruturada.json"
        
        # Constrói o caminho completo usando o diretório fornecido como parâmetro
        filename = os.path.join(output_dir, base_filename)
        
        print(f"Metadados obtidos com sucesso. Salvando em '{filename}'...")
        
        try:
            # Garante que o diretório de saída exista antes de salvar
            os.makedirs(output_dir, exist_ok=True)
            
            # Salva os dados no arquivo
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Arquivo '{filename}' salvo com sucesso.")
        
        except IOError as e:
            print(f"❌ Erro ao salvar o arquivo '{filename}': {e}")
            # Mesmo que não consiga salvar, ainda retornamos os dados
    else:
        print(f"⚠️ Não foi possível obter os metadados para a tabela {table_id}.")

    print("--- FIM DA INSPEÇÃO ---")
    
    # 3. Retorna os dados para quem chamou a função (o run_use_case.py)
    return data