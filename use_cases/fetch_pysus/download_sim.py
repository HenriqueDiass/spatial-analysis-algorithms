# use_cases/fetch_pysus/download_sim.py

import pandas as pd
from pysus import SIM
from typing import List, Optional, Tuple
from shared import pysus_tools

def execute(group_code: str, years: List[int], states: Optional[List[str]] = None) -> Tuple[pd.DataFrame, list]:
    """
    Busca dados do SIM, otimizando a busca por estados e lidando
    corretamente com o retorno da função de download.
    """
    try:
        print(f"➡️  Iniciando busca no SIM para o grupo '{group_code}'...")
        sim = SIM().load()

        # Pede para a biblioteca encontrar os arquivos, já tentando filtrar por estado para otimizar.
        files_to_download = sim.get_files(group=group_code, year=years, uf=states)

        if not files_to_download:
            print("⚠️  Nenhum arquivo encontrado."); return pd.DataFrame(), []

        print(f"📂 {len(files_to_download)} arquivo(s) para baixar. Iniciando download...")
        downloaded_objects = sim.download(files_to_download)
        
        print("🔄  Processando para DataFrame...")
        if isinstance(downloaded_objects, list):
            list_of_dataframes = [pq.to_dataframe() for pq in downloaded_objects]
            unfiltered_df = pd.concat(list_of_dataframes, ignore_index=True) if list_of_dataframes else pd.DataFrame()
        else:
            unfiltered_df = downloaded_objects.to_dataframe()

        # A filtragem manual continua como uma garantia.
        print(f"ℹ️  Aplicando filtro para o(s) estado(s): {states or 'Nenhum'}...")
        filtered_df = pysus_tools.filter_dataframe_by_states(unfiltered_df, states, 'CODMUNOCOR')

        print("🔢  Calculando óbitos por município...")
        cases_per_municipality = []
        if 'CODMUNOCOR' in filtered_df.columns:
            counts = filtered_df.dropna(subset=['CODMUNOCOR'])['CODMUNOCOR'].value_counts()
            cases_per_municipality = [{"codigo_municipio": str(idx), "casos": int(val)} for idx, val in counts.items()]
            print("✅  Contagem concluída.")
        else:
            print("ℹ️  Não foi possível calcular os casos por município (coluna não encontrada).")

        print(f"✅  Processo concluído! {len(filtered_df)} registros foram carregados.")
        return filtered_df, cases_per_municipality
    except Exception as e:
        print(f"❌  Ocorreu um erro durante a busca no SIM: {e}")
        return pd.DataFrame(), []