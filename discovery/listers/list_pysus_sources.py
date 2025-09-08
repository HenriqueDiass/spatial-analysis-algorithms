# use_cases/discovery/listers/list_pysus_sources.py
from shared.display_utils import print_formatted_list

def execute() -> None:
    print("\nListing known data sources from PySUS...")
    
    # Lista manual das fontes de dados mais comuns do PySUS
    known_pysus_sources = [
        "SINAN - Sistema de Informação de Agravos de Notificação",
        "SIM - Sistema de Informações sobre Mortalidade",
        "SIH - Sistema de Informações Hospitalares do SUS",
        "SINASC - Sistema de Informações sobre Nascidos Vivos",
        "CNES - Cadastro Nacional de Estabelecimentos de Saúde",
        "CIHA - Comunicação de Internação Hospitalar"
    ]
    
    print_formatted_list("Available Data Sources in PySUS", known_pysus_sources)