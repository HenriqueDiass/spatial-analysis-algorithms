# use_cases/fetch_pysus/download_cnes.py
import pandas as pd
from pysus.ftp.databases import CNES
from typing import List, Optional

def execute(group_code: str, years: List[int], states: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Busca dados do CNES. Por ser um sistema simples, retorna apenas o DataFrame.
    """
    try:
        print(f"➡️  Iniciando busca no CNES para o grupo '{group_code}'...")
        cnes = CNES().load()
        
        print("🔎  Procurando arquivos...")
        files_to_download = cnes.get_files(group=group_code, uf=states, year=years)

        if not files_to_download:
            print("⚠️  Nenhum arquivo encontrado para os parâmetros informados.")
            return pd.DataFrame()

        print(f"📂 {len(files_to_download)} arquivo(s) encontrado(s). Iniciando download...")
        downloaded_objects = cnes.download(files_to_download)
        
        print("🔄  Processando e concatenando arquivos...")
        list_of_dataframes = [pq.to_dataframe() for pq in downloaded_objects]
        
        if not list_of_dataframes:
            return pd.DataFrame()
            
        consolidated_df = pd.concat(list_of_dataframes, ignore_index=True)
        print(f"✅  Processo concluído! {len(consolidated_df)} registros foram carregados.")
        return consolidated_df
        
    except Exception as e:
        print(f"❌  Ocorreu um erro durante a busca no CNES: {e}")
        return pd.DataFrame()