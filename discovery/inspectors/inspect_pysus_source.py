# use_cases/discovery/inspectors/inspect_pysus_source.py
"""
Use case to inspect a specific PySUS data source and list its contents.
This version uses the native metadata attributes from the pysus library
(e.g., .diseases, .groups) to provide the information dynamically.
"""

# Importa os módulos das fontes de dados que serão inspecionadas
from pysus.online_data import SINAN, SIH, SIA, SIM, SINASC, CNES
from shared.display_utils import print_formatted_list

def execute(source_name: str) -> None:
    """
    Fornece detalhes para uma fonte de dados PySUS, priorizando os metadados nativos da biblioteca.
    """
    source_name = source_name.upper()
    print(f"\nInspecting PySUS data source: {source_name}...")
    
    try:
        if source_name == 'SINAN':
            # --- CORREÇÃO APLICADA AQUI ---
            # Acessa a classe SINAN de DENTRO do módulo SINAN
            # O dicionário .diseases é um atributo da classe, não do módulo.
            SourceClass = getattr(SINAN, 'SINAN')
            items = [f"{v} (Sigla: {k})" for k, v in sorted(SourceClass.diseases.items())]
            print_formatted_list("Doenças (Agravos) Disponíveis no SINAN", items)

        elif source_name in ['SIH', 'SIA', 'SIM', 'SINASC', 'CNES']:
            # Padrão genérico para todas as outras fontes que precisam de .load()
            
            # 1. Obtém o módulo (ex: o módulo SIH) a partir dos módulos já importados
            SourceModule = globals()[source_name]
            
            # 2. Obtém a classe (ex: a classe SIH) de DENTRO do módulo
            SourceClass = getattr(SourceModule, source_name)
            
            # 3. Agora, instancia a CLASSE corretamente
            print(f"Carregando metadados de {source_name} do DATASUS (pode levar um momento)...")
            source_instance = SourceClass()
            source_instance.load()
            
            # 4. Extrai o título e os itens dos atributos nativos da biblioteca
            title = source_instance.metadata.get('long_name', source_name)
            items = [f"{k}: {v}" for k, v in source_instance.groups.items() if v]
            
            # 5. Exibe a lista formatada
            print_formatted_list(title, items)
        
        else:
            print(f"ERROR: Source '{source_name}' is invalid or not recognized.")
            print("You can see available sources by running 'list_pysus_sources'.")

    except Exception as e:
        print(f"ERROR: An unexpected error occurred while inspecting {source_name}. Details: {e}")
        print("Verifique sua conexão com a internet, pois a operação pode depender de acesso ao FTP do DATASUS.")