# run_use_case.py

# Importamos todas as classes que vamos usar
from use_cases import (
    FetchStatesUseCase,
    FetchMunicipalitiesUseCase,
    FetchImmediateRegionsUseCase, 
    FetchIntermediateRegionsUseCase, 
)

# --- Funções Auxiliares para cada Tarefa ---
# Manter estas funções separadas deixa o menu principal mais limpo.

def run_states():
    """Executa o caso de uso para buscar dados dos estados."""
    print("\n--- Iniciando Tarefa: DADOS COMPLETOS POR ESTADO ---")
    uc = FetchStatesUseCase()
    uc.execute(output_filename="1-dados-completos-estados.geojson")
    print("--- Tarefa Concluída! ---")

def run_municipalities():
    """Pede a sigla do estado e executa o caso de uso de municípios."""
    uf = input("  -> Digite a sigla do Estado (UF) que você quer buscar (ex: PE, SP, RJ): ").upper()
    if not uf or len(uf) != 2:
        print("  -> Sigla de estado inválida. Voltando ao menu.")
        return
        
    print(f"\n--- Iniciando Tarefa: MUNICÍPIOS DE {uf} ---")
    uc = FetchMunicipalitiesUseCase()
    uc.execute(
        sigla_uf=uf, 
        output_filename=f"2-dados-completos-municipios-{uf.lower()}.geojson"
    )
    print("--- Tarefa Concluída! ---")

def run_immediate_regions():
    """Executa o caso de uso para buscar dados das regiões imediatas."""
    print("\n--- Iniciando Tarefa: REGIÕES IMEDIATAS DO BRASIL ---")
    uc = FetchImmediateRegionsUseCase()
    uc.execute(output_filename="3-regioes-imediatas.geojson")
    print("--- Tarefa Concluída! ---")

def run_intermediate_regions():
    """Executa o caso de uso para buscar dados das regiões intermediárias."""
    print("\n--- Iniciando Tarefa: REGIÕES INTERMEDIÁRIAS DO BRASIL ---")
    uc = FetchIntermediateRegionsUseCase()
    uc.execute(output_filename="4-regioes-intermediarias.geojson")
    print("--- Tarefa Concluída! ---")

def display_menu():
    """Mostra o menu de opções para o usuário."""
    print("\n+------------------------------------------------------+")
    print("|            PAINEL DE CONTROLE DE COLETA              |")
    print("+------------------------------------------------------+")
    print("| 1. Baixar Dados Completos dos Estados                |")
    print("| 2. Baixar Dados dos Municípios (por Estado)          |")
    print("| 3. Baixar Dados das Regiões Imediatas                |")
    print("| 4. Baixar Dados das Regiões Intermediárias           |")
    print("| 5. RODAR TUDO em sequência                           |")
    print("| 0. Sair do programa                                  |")
    print("+------------------------------------------------------+")

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    
    # Loop infinito que mantém o menu ativo até o usuário decidir sair
    while True:
        display_menu()
        escolha = input("Digite o número da sua escolha e pressione Enter: ")

        try:
            # O painel de IF/ELSE que você sugeriu
            if escolha == '1':
                run_states()
            
            elif escolha == '2':
                run_municipalities()

            elif escolha == '3':
                run_immediate_regions()

            elif escolha == '4':
                run_intermediate_regions()

            elif escolha == '5':
                print("\n--- ATENÇÃO: Executando todas as tarefas em sequência. ---")
                run_states()
                run_municipalities() # Vai pedir o estado quando chegar aqui
                run_immediate_regions()
                run_intermediate_regions()
                print("\n🎉 TODAS AS TAREFAS FORAM EXECUTADAS! 🎉")

            elif escolha == '0':
                print("Saindo do programa. Até logo!")
                break # Quebra o loop e encerra o programa
            
            else:
                print("Opção inválida! Por favor, escolha um número do menu.")

        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado durante a execução: {e}")
            print("Retornando ao menu principal...")

        # Pausa para o usuário ler a saída antes de mostrar o menu novamente
        input("\nPressione Enter para continuar...")
