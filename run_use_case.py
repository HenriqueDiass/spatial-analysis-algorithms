import sys
import os

# =============================================================================
# SEÇÃO 1: CONFIGURAÇÃO DE AMBIENTE E CAMINHOS
# =============================================================================
# Define o diretório raiz do projeto e os caminhos para as pastas principais
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SHARED_DIR = os.path.join(PROJECT_ROOT, "shared")
# Adiciona o diretório raiz ao path do Python para permitir importações diretas
sys.path.insert(0, PROJECT_ROOT)

# =============================================================================
# SEÇÃO 2: IMPORTAÇÕES DOS MÓDULOS E USE CASES
# =============================================================================
try:
    # --- Módulos Compartilhados ---
    from shared import pysus_tools, output_manager

    # --- Módulos de Descoberta (Importação Explícita para evitar conflitos) ---
    from discovery import listers
    # Importamos os módulos de inspeção do PySUS um por um
    from discovery.inspectors import cnes_inspector
    from discovery.inspectors import sia_inspector
    from discovery.inspectors import sih_inspector
    from discovery.inspectors import sim_inspector
    from discovery.inspectors import sinan_inspector
    from discovery.inspectors import sinasc_inspector
    # Importamos os inspetores originais do seu projeto
    from discovery import inspectors as sidrapy_inspectors # Damos um apelido para não confundir

    # --- Use Cases de Fetch e Geração ---
    from use_cases.fetch_pysus import (
        download_cnes,
        download_sia,
        download_sih,
        download_sim,
        download_sinan,
        download_sinasc
    )
    from use_cases import (
        FetchStatesUseCase, FetchMunicipalitiesUseCase, FetchImmediateRegionsUseCase, FetchIntermediateRegionsUseCase,
        gerar_mapa_destaque_geobr
    )
    from use_cases.map_generators import (
        gerar_mapa_destaque, 
        gerar_mapa_zoom,
        gerar_mapa_municipios_coropleth,
        gerar_mapa_estados_coropleth,
        gerar_mapa_regional_estado
    )
    from use_cases.map_generators.generate_clipped_regions_map import execute as gerar_mapa_regioes_recortadas
    
except ImportError as e:
    print(f"ERRO DE IMPORTAÇÃO: {e}\nVerifique se todas as pastas e arquivos '__init__.py' estão corretos.")
    sys.exit(1)

# Bloco para verificar a disponibilidade das bibliotecas de mapa
try:
    import matplotlib.pyplot as plt
    MAPS_AVAILABLE = True
except ImportError:
    MAPS_AVAILABLE = False
    print("\nAVISO: Bibliotecas de mapa (matplotlib, geopandas) não encontradas. Funções de mapa desativadas.")

# =============================================================================
# SEÇÃO 3: CONTROLADORES DE TAREFAS
# =============================================================================

# --- Controladores de Fetch (GeoBR) ---
def run_states():
    print("\n--- Tarefa: DADOS COMPLETOS POR ESTADO ---")
    output_filename = os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson")
    if os.path.exists(output_filename):
        if input(f"   -> Arquivo já existe. Baixar novamente? (s/n): ").lower() != 's':
            print("       Download pulado."); return
    uc = FetchStatesUseCase()
    uc.execute(output_filename=output_filename)
    print("--- Tarefa Concluída! ---")

def run_municipalities():
    uf = input("   -> Digite a Sigla do Estado (ex: PE, SP, RJ): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    print(f"\n--- Tarefa: MUNICÍPIOS DE {uf} ---")
    output_filename = os.path.join(OUTPUT_DIR, f"2-complete-data-municipalities-{uf.lower()}.geojson")
    if os.path.exists(output_filename):
        if input(f"   -> Arquivo já existe. Baixar novamente? (s/n): ").lower() != 's':
            print("       Download pulado."); return
    uc = FetchMunicipalitiesUseCase()
    uc.execute(state_abbreviation=uf, output_filename=output_filename)
    print("--- Tarefa Concluída! ---")

def run_immediate_regions():
    print("\n--- Tarefa: REGIÕES IMEDIATAS DO BRASIL ---")
    output_filename = os.path.join(OUTPUT_DIR, "3-immediate-regions.geojson")
    if os.path.exists(output_filename):
        if input(f"   -> Arquivo já existe. Baixar novamente? (s/n): ").lower() != 's':
            print("       Download pulado."); return
    uc = FetchImmediateRegionsUseCase()
    uc.execute(output_filename=output_filename)
    print("--- Tarefa Concluída! ---")

def run_intermediate_regions():
    print("\n--- Tarefa: REGIÕES INTERMEDIÁRIAS DO BRASIL ---")
    output_filename = os.path.join(OUTPUT_DIR, "4-intermediate-regions.geojson")
    if os.path.exists(output_filename):
        if input(f"   -> Arquivo já existe. Baixar novamente? (s/n): ").lower() != 's':
            print("       Download pulado."); return
    uc = FetchIntermediateRegionsUseCase()
    uc.execute(output_filename=output_filename)
    print("--- Tarefa Concluída! ---")

# --- Controladores de Fetch (PySUS) - **ATUALIZADOS** ---
# run_use_case.py (substituir as 6 funções de fetch do PySUS por estas)

def run_fetch_cnes_controller():
    print("\n--- Tarefa: Baixar dados do CNES (PySUS) ---")
    params = cnes_inspector.get_cnes_parameters() # Assume que você criou este arquivo
    if params is None:
        print("\nOperação cancelada."); return
    print("\nParâmetros validados. Iniciando a busca dos dados...")
    data_results = download_cnes.execute(**params)
    output_manager.save_cnes_output(OUTPUT_DIR, params, data_results)
    print("--- Tarefa Concluída! ---")

def run_fetch_sia_controller():
    print("\n--- Tarefa: Baixar dados do SIA (PySUS) ---")
    params = sia_inspector.get_sia_parameters() # Assume que você criou este arquivo
    if params is None:
        print("\nOperação cancelada."); return
    print("\nParâmetros validados. Iniciando a busca dos dados...")
    data_results = download_sia.execute(**params)
    output_manager.save_sia_output(OUTPUT_DIR, params, data_results)
    print("--- Tarefa Concluída! ---")

def run_fetch_sih_controller():
    print("\n--- Tarefa: Baixar dados do SIH (PySUS) ---")
    params = sih_inspector.get_sih_parameters() # Assume que você criou este arquivo
    if params is None:
        print("\nOperação cancelada."); return
    print("\nParâmetros validados. Iniciando a busca dos dados...")
    data_results = download_sih.execute(**params)
    output_manager.save_sih_output(OUTPUT_DIR, params, data_results)
    print("--- Tarefa Concluída! ---")

def run_fetch_sim_controller():
    print("\n--- Tarefa: Baixar dados do SIM (PySUS) ---")
    params = sim_inspector.get_sim_parameters() # Assume que você criou este arquivo
    if params is None:
        print("\nOperação cancelada."); return
    print("\nParâmetros validados. Iniciando a busca dos dados...")
    data_results = download_sim.execute(**params)
    output_manager.save_sim_output(OUTPUT_DIR, params, data_results)
    print("--- Tarefa Concluída! ---")
    
def run_fetch_sinasc_controller():
    print("\n--- Tarefa: Baixar dados do SINASC (PySUS) ---")
    params = sinasc_inspector.get_sinasc_parameters() # Assume que você criou este arquivo
    if params is None:
        print("\nOperação cancelada."); return
    print("\nParâmetros validados. Iniciando a busca dos dados...")
    data_results = download_sinasc.execute(**params)
    output_manager.save_sinasc_output(OUTPUT_DIR, params, data_results)
    print("--- Tarefa Concluída! ---")
    
def run_fetch_sinan_controller():
    print("\n--- Tarefa: Baixar dados do SINAN (PySUS) ---")
    params = sinan_inspector.get_sinan_parameters()
    if params is None:
        print("\nOperação cancelada."); return
    print("\nParâmetros validados. Iniciando a busca dos dados...")
    data_results = download_sinan.execute(**params)
    output_manager.save_sinan_output(OUTPUT_DIR, params, data_results)
    print("--- Tarefa Concluída! ---")

# --- Controladores de Descoberta e Inspeção (Listers e Inspectors) ---
def run_list_geobr_controller():
    print("\n--- Ferramenta: Listar Datasets do GeoBR ---")
    listers.list_geobr_datasets()

def run_list_pysus_controller():
    print("\n--- Ferramenta: Listar Fontes de Dados do PySUS ---")
    listers.list_pysus_sources()

def run_list_sidrapy_controller():
    print("\n--- Ferramenta: Listar Todas as Tabelas do Sidrapy (IBGE) ---")
    listers.list_sidrapy_tables()

def run_list_states_controller():
    print("\n--- Ferramenta: Listar Estados Brasileiros (via GeoBR) ---")
    listers.list_brazilian_states()

def run_inspect_sidrapy_controller():
    print("\n--- Ferramenta: Inspecionar Tabela do Sidrapy ---")
    table_code = input("   -> Digite o código da tabela para inspecionar (ex: 6579): ")
    if not table_code.isdigit(): print("   -> Código da tabela deve ser um número."); return
    sidrapy_inspectors.inspect_sidrapy_table(table_code)

def run_inspect_pysus_controller():
    print("\n--- Ferramenta: Inspecionar Fonte do PySUS ---")
    print("Qual fonte de dados do PySUS você deseja inspecionar?")
    print(" 1. CNES\n 2. SIA\n 3. SIH\n 4. SIM\n 5. SINAN\n 6. SINASC")
    choice = input(" -> Escolha uma opção: ")
    
    inspector_map = {
        '1': cnes_inspector, '2': sia_inspector, '3': sih_inspector,
        '4': sim_inspector, '5': sinan_inspector, '6': sinasc_inspector,
    }
    
    inspector_module = inspector_map.get(choice)
    if inspector_module:
        inspector_module.show_available_options()
    else:
        print("Opção inválida!")


# --- Controladores de Mapa (Mantidos do seu script original) ---
def run_map_destaque_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Sigla do Estado para destacar (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    caminhos = {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson"), 'saida': os.path.join(OUTPUT_DIR, f"mapa_destaque_{uf.lower()}.png")}
    if not os.path.exists(caminhos['estados']): print("\nAVISO: Arquivo de estados não encontrado. Execute a Opção 1."); return
    gerar_mapa_destaque(uf, caminhos)

def run_map_destaque_geobr_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Sigla do Estado para destacar (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    caminhos = {
        'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 
        'saida': os.path.join(OUTPUT_DIR, f"mapa_destaque_geobr_{uf.lower()}.png")
    }
    if not os.path.exists(caminhos['sulamerica']): 
        print(f"\nAVISO: Arquivo de base '{caminhos['sulamerica']}' não encontrado."); return
    gerar_mapa_destaque_geobr(uf, caminhos)

def run_map_zoom_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Sigla do Estado para mapa com zoom (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    caminhos = {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson"), 'municipios': os.path.join(OUTPUT_DIR, f"2-complete-data-municipalities-{uf.lower()}.geojson"), 'saida': os.path.join(OUTPUT_DIR, f"mapa_zoom_municipios_{uf.lower()}.png")}
    if not os.path.exists(caminhos['estados']): print("\nAVISO: Arquivo de estados não encontrado (Opção 1)."); return
    if not os.path.exists(caminhos['municipios']): print(f"\nAVISO: Arquivo de municípios para {uf} não encontrado (Opção 2)."); return
    gerar_mapa_zoom(uf, caminhos)

def run_municipalities_choropleth_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Sigla do Estado para o mapa coroplético (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    coluna = input(f"   -> Qual coluna dos municípios de {uf} usar para as cores? (ex: population): ").lower()
    if not coluna: print("   -> Nome da coluna não pode ser vazio."); return
    caminhos = {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson"), 'municipios': os.path.join(OUTPUT_DIR, f"2-complete-data-municipalities-{uf.lower()}.geojson"), 'saida': os.path.join(OUTPUT_DIR, f"mapa_coropleth_municipios_{uf.lower()}_{coluna}.png")}
    if not os.path.exists(caminhos['estados']): print("\nAVISO: Arquivo de estados não encontrado (Opção 1)."); return
    if not os.path.exists(caminhos['municipios']): print(f"\nAVISO: Arquivo de municípios para {uf} não encontrado (Opção 2)."); return
    gerar_mapa_municipios_coropleth(uf, coluna, caminhos)

def run_states_choropleth_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    coluna = input("   -> Qual coluna do arquivo de estados usar para as cores? (ex: population): ").lower()
    if not coluna: print("   -> Nome da coluna não pode ser vazio."); return
    caminhos = {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson"), 'saida': os.path.join(OUTPUT_DIR, f"mapa_coropleth_estados_{coluna}.png")}
    if not os.path.exists(caminhos['estados']): print("\nAVISO: Arquivo de estados não encontrado (Opção 1)."); return
    gerar_mapa_estados_coropleth(coluna, caminhos)

def run_state_regional_map_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Digite a Sigla do Estado para ver suas divisões (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    print("\nVerificando arquivos para o mapa de divisões...")
    caminhos = {
        'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson"),
        'municipios': os.path.join(OUTPUT_DIR, f"2-complete-data-municipalities-{uf.lower()}.geojson"), 'imediatas': os.path.join(OUTPUT_DIR, "3-immediate-regions.geojson"),
        'intermediarias': os.path.join(OUTPUT_DIR, "4-intermediate-regions.geojson"), 'saida': os.path.join(OUTPUT_DIR, f"mapa_divisoes_{uf.lower()}.png")
    }
    arquivos_obrigatorios = {'estados': "Opção 1", 'imediatas': "Opção 3", 'intermediarias': "Opção 4"}
    arquivos_faltando = False
    for key, opcao in arquivos_obrigatorios.items():
        if not os.path.exists(caminhos[key]):
            print(f"   -> ERRO: Arquivo obrigatório de '{key}' não foi encontrado.")
            print(f"   -> Por favor, execute a '{opcao}' no menu principal primeiro.")
            arquivos_faltando = True
    if arquivos_faltando: return
    gerar_mapa_regional_estado(uf, caminhos)

def run_clipped_regions_map_controller():
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Digite a Sigla do Estado para o mapa (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    region_choice = input("   -> Qual tipo de região? (1 para Imediatas, 2 para Intermediárias): ")
    if region_choice == '1':
        region_type = 'imediatas'; required_file = 'imediatas'; required_option = 'Opção 3'
    elif region_choice == '2':
        region_type = 'intermediarias'; required_file = 'intermediarias'; required_option = 'Opção 4'
    else:
        print("   -> Escolha inválida. Use 1 ou 2."); return
    print(f"\nVerificando arquivos para o mapa de Regiões {region_type.capitalize()}...")
    caminhos = {
        'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson"),
        'imediatas': os.path.join(OUTPUT_DIR, "3-immediate-regions.geojson"), 'intermediarias': os.path.join(OUTPUT_DIR, "4-intermediate-regions.geojson"),
        'saida': os.path.join(OUTPUT_DIR, f"mapa_regiao_{region_type}_{uf.lower()}.png")
    }
    if not os.path.exists(caminhos['estados']): print("   -> ERRO: Arquivo de 'estados' não foi encontrado. Execute a 'Opção 1'."); return
    if not os.path.exists(caminhos[required_file]): print(f"   -> ERRO: Arquivo de '{required_file}' não foi encontrado. Execute a '{required_option}'."); return
    gerar_mapa_regioes_recortadas(uf=uf, caminhos=caminhos, region_type=region_type)

def run_all_maps_for_state_controller():
    # Esta função parece estar faltando no seu loop principal, mas mantive a lógica aqui
    if not MAPS_AVAILABLE: print("Funcionalidade de mapas indisponível."); return
    uf = input("   -> Digite a Sigla do Estado para o relatório completo (ex: PE): ").upper()
    if not uf or len(uf) != 2: print("   -> Sigla inválida."); return
    coluna = input(f"   -> Qual coluna usar para o mapa coroplético de {uf}? (ex: population): ").lower()
    if not coluna: print("   -> Nome da coluna não pode ser vazio."); return
    print(f"\n--- Iniciando Relatório Completo de Mapas para {uf} ---")
    caminho_estados = os.path.join(OUTPUT_DIR, "1-complete-data-states.geojson")
    caminho_municipios = os.path.join(OUTPUT_DIR, f"2-complete-data-municipalities-{uf.lower()}.geojson")
    if not os.path.exists(caminho_estados) or not os.path.exists(caminho_municipios):
        print("\nAVISO: Arquivos de dados necessários não encontrados. Execute as Opções 1 e 2."); return
    gerar_mapa_destaque(uf, {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': caminho_estados, 'saida': os.path.join(OUTPUT_DIR, f"mapa_destaque_{uf.lower()}.png")})
    gerar_mapa_zoom(uf, {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': caminho_estados, 'municipios': caminho_municipios, 'saida': os.path.join(OUTPUT_DIR, f"mapa_zoom_municipios_{uf.lower()}.png")})
    gerar_mapa_municipios_coropleth(uf, coluna, {'sulamerica': os.path.join(SHARED_DIR, "south_america.geojson"), 'estados': caminho_estados, 'municipios': caminho_municipios, 'saida': os.path.join(OUTPUT_DIR, f"mapa_coropleth_municipios_{uf.lower()}_{coluna}.png")})
    print(f"\n🎉 Relatório completo para {uf} finalizado! 3 mapas foram salvos em 'output'. 🎉")


# =============================================================================
# SEÇÃO 4: INTERFACE COM O USUÁRIO E LOOP PRINCIPAL
# =============================================================================
def display_menu():
    print("\n+---------------------------------------------------------+")
    print("|           PAINEL DE CONTROLE DE DADOS E MAPAS           |")
    print("+---------------------------------------------------------+")
    print("| DADOS GEOJSON (GeoBR)                                   |")
    print("|  1. Baixar Dados dos Estados                            |")
    print("|  2. Baixar Dados dos Municípios (por Estado)            |")
    print("|  3. Baixar Dados das Regiões Imediatas                  |")
    print("|  4. Baixar Dados das Regiões Intermediárias             |")
    print("|  5. EXECUTAR TODOS OS FETCHS (Exceto Municípios)        |")
    print("+---------------------------------------------------------+")
    print("| DESCOBERTA E INSPEÇÃO DE DADOS                          |")
    print("| 12. Listar Datasets disponíveis no GeoBR                |")
    print("| 13. Listar Fontes de Dados do PySUS                     |")
    print("| 14. Listar TODAS as Tabelas do Sidra (Pode ser lento)   |")
    print("| 16. Inspecionar Tabela do Sidrapy (ver variáveis)       |")
    print("| 17. Inspecionar Fonte do PySUS (ver detalhes)           |")
    print("| 18. Listar Estados Brasileiros (Nome, Sigla, Código)    |")
    print("+---------------------------------------------------------+")
    print("| DOWNLOAD DE DADOS BRUTOS (PySUS)                        |")
    print("| 31. Baixar dados do CNES                                |")
    print("| 32. Baixar dados do SIA                                 |")
    print("| 33. Baixar dados do SIH                                 |")
    print("| 34. Baixar dados do SIM                                 |")
    print("| 35. Baixar dados do SINASC                              |")
    print("| 36. Baixar dados do SINAN                               |")
    if MAPS_AVAILABLE:
        print("+---------------------------------------------------------+")
        print("| MAPAS                                                   |")
        print("| 21. Gerar Mapa de Destaque (Usa dados baixados)         |")
        print("| 22. Gerar Mapa com Zoom dos Municípios                  |")
        print("| 23. Gerar Mapa Coroplético de Municípios                |")
        print("| 24. Gerar Mapa Coroplético dos Estados                  |")
        print("| 25. Gerar Mapa de Divisões Regionais de um Estado       |")
        print("| 26. Gerar Mapa de Regiões Recortadas (Imed./Interm.)    |")
        print("| 27. Gerar Relatório Completo para um Estado             |") # Mantive esta opção, embora não esteja no seu loop.
        print("| 28. Gerar Mapa de Destaque (com GeoBR - Online)         |")
    print("+---------------------------------------------------------+")
    print("|  0. Sair do programa                                    |")
    print("+---------------------------------------------------------+")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Mapeamento de escolhas para funções
    actions = {
        '1': run_states, '2': run_municipalities, '3': run_immediate_regions, '4': run_intermediate_regions,
        '5': lambda: (print("\n--- ATENÇÃO: Executando todos os fetchs de dados. ---"),
                      run_states(), run_immediate_regions(), run_intermediate_regions(),
                      print("\nPara baixar os municípios, execute a opção 2 individualmente."),
                      print("\n🎉 TAREFAS DE FETCH CONCLUÍDAS! 🎉")),
        '12': run_list_geobr_controller, '13': run_list_pysus_controller, '14': run_list_sidrapy_controller,
        '16': run_inspect_sidrapy_controller, '17': run_inspect_pysus_controller, '18': run_list_states_controller,
        '31': run_fetch_cnes_controller, '32': run_fetch_sia_controller, '33': run_fetch_sih_controller,
        '34': run_fetch_sim_controller, '35': run_fetch_sinasc_controller, '36': run_fetch_sinan_controller,
    }

    if MAPS_AVAILABLE:
        map_actions = {
            '21': run_map_destaque_controller, '22': run_map_zoom_controller, '23': run_municipalities_choropleth_controller,
            '24': run_states_choropleth_controller, '25': run_state_regional_map_controller, '26': run_clipped_regions_map_controller,
            '27': run_all_maps_for_state_controller, '28': run_map_destaque_geobr_controller,
        }
        actions.update(map_actions)

    while True:
        display_menu()
        choice = input("Digite o número da sua escolha e pressione Enter: ")
        
        if choice == '0':
            print("Saindo do programa. Até logo!"); break

        action_to_run = actions.get(choice)
        
        if action_to_run:
            try:
                action_to_run()
            except Exception as e:
                print(f"\n❌ Ocorreu um erro inesperado: {e}")
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")