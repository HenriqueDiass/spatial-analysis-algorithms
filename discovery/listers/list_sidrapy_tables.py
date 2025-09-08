"""
Use case to dynamically fetch and display ALL Sidra (IBGE) tables,
grouped by their parent survey, from the official IBGE 'agregados' API endpoint.
"""
import requests

# A URL CORRETA que você forneceu, que já inclui as tabelas (agregados)
SIDRA_TABLES_API_URL = 'https://servicodados.ibge.gov.br/api/v3/agregados'

def execute() -> None:
    
    print("\nAviso: Buscando a lista COMPLETA de pesquisas e tabelas do IBGE...")
    
    try:
        # Faz a requisição para o endpoint que contém todas as tabelas
        response = requests.get(SIDRA_TABLES_API_URL, timeout=30)
        response.raise_for_status()  # Lança um erro para respostas com status 4xx ou 5xx
        
        # A resposta JSON já é a lista de pesquisas com os agregados dentro
        data_from_api = response.json()

        if not data_from_api:
            print("Nenhuma pesquisa ou tabela foi encontrada na API do IBGE.")
            return

        # Itera sobre cada item da lista (cada item é uma 'pesquisa')
        for survey in data_from_api:
            survey_name = survey.get('nome', 'Pesquisa sem nome')
            
            # Imprime o título da Pesquisa-mãe
            print(f"\n--- PESQUISA: {survey_name} ---")

            # Pega a lista de 'agregados' (tabelas) de dentro da pesquisa
            tables = survey.get('agregados', [])
            
            if not tables:
                print("    (Nenhuma tabela/agregado listado para esta pesquisa)")
                continue

            # Itera e imprime cada tabela com seu código e nome
            for table in tables:
                table_id = table.get('id', 'N/A')
                table_name = table.get('nome', 'Tabela sem nome')
                print(f"    Código: {table_id} | Tabela: {table_name}")

    except requests.exceptions.RequestException as e:
        print(f"ERRO: Não foi possível conectar à API do IBGE. Verifique sua conexão. Detalhes: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a busca: {e}")