# use_cases/fetch_pysus/download_sih.py
import pandas as pd
from pysus.ftp.databases import SIH
from typing import List, Optional

def execute(group_code: str, years: List[int], states: Optional[List[str]] = None, months: Optional[List[int]] = None) -> pd.DataFrame:
    """
    Busca dados do SIH. Por ser um sistema simples, retorna apenas o DataFrame.
    """
    try:
        print(f"➡️  Iniciando busca no SIH para o grupo '{group_code}'...")
        sih = SIH().load()
        
        print("🔎  Procurando arquivos...")
        files_to_download = sih.get_files(group=group_code, uf=states, year=years, month=months)

        if not files_to_download:
            print("⚠️  Nenhum arquivo encontrado para os parâmetros informados.")
            return pd.DataFrame()

        print(f"📂 {len(files_to_download)} arquivo(s) encontrado(s). Iniciando download...")
        downloaded_data_set = sih.download(files_to_download)
        
        print("🔄  Processando para DataFrame...")
        dataframe = downloaded_data_set.to_dataframe()
        print(f"✅  Processo concluído! {len(dataframe)} registros foram carregados.")
        return dataframe
        
    except Exception as e:
        print(f"❌  Ocorreu um erro durante a busca no SIH: {e}")
        return pd.DataFrame()