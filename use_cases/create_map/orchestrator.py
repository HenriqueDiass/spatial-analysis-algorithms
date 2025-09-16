import os
from use_cases.data_processing import process_birth_rate_data
from . import plotter

def execute(pysus_output_dir: str, map_output_dir: str):
    """
    Orquestra o fluxo completo de geração de um mapa coroplético.
    """
    print("\n--- Tarefa: Gerar Mapa Coroplético ---")
    
    state_abbr = input("  -> Digite a Sigla do Estado (ex: PE): ").upper()
    year_str = input(f"  -> Digite o ano da análise (ex: 2022): ")
    
    if not (state_abbr and year_str.isdigit() and len(year_str) == 4):
        print("❌ ERRO: Estado ou ano inválido."); return
    
    year = int(year_str)

    sinasc_file = os.path.join(pysus_output_dir, f"pysus_sinasc_summary_DN_{year}_{state_abbr}.json")
    pop_file = os.path.join(pysus_output_dir, f"ibge_population_{state_abbr}_{year}_censo.json")
    
    gdf_final = process_birth_rate_data.execute(
        state_abbr=state_abbr, year=year,
        sinasc_json_path=sinasc_file, 
        population_json_path=pop_file
    )
    
    if gdf_final is None: return

    print("\nEscolha a métrica para visualizar no mapa:")
    print("  1 - Total de Nascimentos\n  2 - População Estimada\n  3 - Taxa de Natalidade (por 1.000 hab.)")
    print("  --- Nascimentos por Faixa Etária da Mãe ---")
    print("  4 - Mães com menos de 20 anos\n  5 - Mães com 20 a 29 anos\n  6 - Mães com 30 a 39 anos\n  7 - Mães com 40 anos ou mais")
    escolha = input("Digite o número da opção desejada: ")
    
    if escolha == '1':
        column, title, legend = 'total_nascimentos', f'Total de Nascimentos - {state_abbr} ({year})', 'Nascimentos'
    elif escolha == '2':
        column, title, legend = 'population', f'População Estimada - {state_abbr} ({year})', 'Habitantes'
    elif escolha == '3':
        column, title, legend = 'taxa_natalidade_por_mil', f'Taxa de Natalidade - {state_abbr} ({year})', 'Nasc. por 1.000 hab.'
    elif escolha == '4':
        column, title, legend = 'nascimentos_menor20', f'Nascimentos (Mães < 20 anos) - {state_abbr} ({year})', 'Nascimentos'
    elif escolha == '5':
        column, title, legend = 'nascimentos_20a29', f'Nascimentos (Mães 20-29 anos) - {state_abbr} ({year})', 'Nascimentos'
    elif escolha == '6':
        column, title, legend = 'nascimentos_30a39', f'Nascimentos (Mães 30-39 anos) - {state_abbr} ({year})', 'Nascimentos'
    elif escolha == '7':
        column, title, legend = 'nascimentos_40mais', f'Nascimentos (Mães 40+ anos) - {state_abbr} ({year})', 'Nascimentos'
    else:
        print("❌ Opção inválida."); return
        
    output_file = os.path.join(map_output_dir, f"mapa_{column}_{state_abbr}_{year}.png")
    
    # --- MUDANÇA AQUI: Passando o state_abbr para a função de plotagem ---
    plotter.plot(
        gdf=gdf_final, 
        state_abbr=state_abbr, # <<<<<<<<<<<<<<<<<<<< ADICIONADO
        column_to_plot=column,
        title=title, 
        legend_label=legend, 
        output_path=output_file
    )