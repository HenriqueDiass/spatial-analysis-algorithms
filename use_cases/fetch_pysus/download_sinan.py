# use_cases/fetch_pysus/download_sinan.py
import pandas as pd
from pysus import SINAN
from typing import List, Optional, Tuple
from shared import pysus_tools

def execute(disease_code: str, years: List[int], state: Optional[str] = None) -> Tuple[pd.DataFrame, list, str]:
    """
    Busca dados do SINAN, filtra por estado, e calcula casos por município.
    Retorna uma tupla: (DataFrame, lista_de_casos_por_municipio, mensagem_de_filtro)
    """
    try:
        print(f"➡️  Iniciando busca no SINAN para a doença '{disease_code}'...")
        sinan = SINAN().load()
        
        files_to_download = sinan.get_files(dis_code=disease_code, year=years)

        if not files_to_download:
            print("⚠️  Nenhum arquivo encontrado para os parâmetros informados.")
            return pd.DataFrame(), [], "Nenhum arquivo encontrado."

        print(f"📂 {len(files_to_download)} arquivo(s) encontrado(s). Iniciando download...")
        downloaded_set = sinan.download(files_to_download)
        
        print("🔄  Processando para DataFrame...")
        full_dataframe = downloaded_set.to_dataframe()
        dataframe_to_process = full_dataframe
        filter_info_message = "Nenhum filtro de estado aplicado."
        
        if state:
            ibge_code = pysus_tools.STATE_ABBR_TO_IBGE_CODE.get(state.upper())
            if not ibge_code:
                filter_info_message = f"⚠️  Sigla do estado '{state}' inválida. Mostrando todos os dados."
            elif 'SG_UF_NOT' not in full_dataframe.columns:
                filter_info_message = "⚠️  Coluna 'SG_UF_NOT' não encontrada para filtragem. Mostrando todos os dados."
            else:
                mask = full_dataframe['SG_UF_NOT'].astype(str) == ibge_code
                dataframe_to_process = full_dataframe[mask].copy()
                filter_info_message = f"Dados filtrados pelo estado '{state}' (código IBGE: {ibge_code})."
            print(filter_info_message)
        
        print("🔢  Calculando casos por município...")
        cases_per_municipality = []
        municipality_col = next((col for col in ["ID_MN_RESI", "ID_MUNICIP", "ID_MN_NOT"] if col in dataframe_to_process.columns), None)
        
        if municipality_col:
            counts_df = dataframe_to_process.dropna(subset=[municipality_col])
            cases_df = counts_df[municipality_col].value_counts().rename_axis("codigo_municipio").reset_index(name="casos")
            cases_per_municipality = [{"codigo_municipio": str(row["codigo_municipio"]), "casos": int(row["casos"])} for _, row in cases_df.iterrows()]
            print("✅  Contagem concluída.")
        else:
            print("⚠️  Coluna de município não encontrada para gerar a contagem de casos.")

        print(f"✅  Processo concluído! {len(dataframe_to_process)} registros carregados.")
        return dataframe_to_process, cases_per_municipality, filter_info_message
        
    except Exception as e:
        print(f"❌  Ocorreu um erro durante a busca no SINAN: {e}")
        return pd.DataFrame(), [], str(e)