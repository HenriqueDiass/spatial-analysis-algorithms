# use_cases/discovery/inspectors/inspect_sidrapy_table.py
"""
Use case to fetch and display actual data from a specific Sidra (IBGE) table.
"""
import sidrapy
import pandas as pd

def execute(table_code: str) -> None:
    
    print(f"\n--- Buscando dados da tabela Sidra: {table_code} ---")

    # Configura o pandas para exibir melhor as tabelas no console
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    try:
        # Usamos sidrapy.get_table para buscar os dados reais da tabela.
        # Por padrão, buscamos o último período para o Brasil para uma inspeção rápida.
        data = sidrapy.get_table(
            table_code=table_code,
            territorial_level="1",      # Nível Territorial: 1 = Brasil
            ibge_territorial_code="1",  # Código do Território: 1 = Brasil
            variable="all",             # Todas as variáveis da tabela
            period="last 1"             # Período: 'last 1' para o mais recente
        )

        if data is not None and not data.empty:
            print("\n✅ Dados encontrados com sucesso!")
            # Os dados reais começam na segunda linha (índice 1) do DataFrame retornado
            print("A seguir, os dados mais recentes para o nível 'Brasil':")
            print(data.iloc[1:])
        else:
            print(f"\n⚠️ Nenhum dado foi retornado para a tabela {table_code}. Verifique o código ou os parâmetros.")

    except Exception as e:
        print(f"ERRO: Falha ao buscar dados da tabela {table_code}. Detalhes: {e}")
