import pandas as pd
from pysus.ftp.databases import CNES
from typing import List, Optional, Dict

class FetchDataCnesUseCase:
    """
    Caso de uso para buscar dados do CNES e já retornar um resumo agregado por município.
    """
    def execute(self, group_code: str, years: List[int], states: Optional[List[str]] = None, columns: Optional[List[str]] = None) -> Optional[List[Dict]]:
        """
        Executa a busca de dados e o processamento do resumo.

        Retorna:
            Uma lista de dicionários com o total de registros por município.
        """
        try:
            print(f"Buscando dados no CNES para o grupo '{group_code}' para resumir...")
            cnes_db = CNES().load()
            files_to_download = cnes_db.get_files(group=group_code, uf=states, year=years)

            if not files_to_download:
                print("Nenhum arquivo do CNES encontrado.")
                return None

            downloaded_dataset = cnes_db.download(files_to_download)
            if downloaded_dataset is None:
                return None
            
            coluna_municipio = 'CODUFMUN' # Exemplo para o grupo 'ST' (Estabelecimentos)
            dataframe = downloaded_dataset.to_dataframe(columns=[coluna_municipio])
            
            if dataframe.empty:
                return None

            # --- O CÁLCULO DO RESUMO É FEITO AQUI DENTRO ---
            print("Calculando resumo por município...")
            summary_df = dataframe.groupby(coluna_municipio).size().reset_index(name='total')
            
            # Renomeia as colunas para um formato padronizado
            summary_df.rename(columns={coluna_municipio: 'municipality_code'}, inplace=True)
            
            print(f"Resumo do CNES gerado para {len(summary_df)} municípios.")
            
            # Retornamos apenas a lista com o resumo, e não o DataFrame gigante
            return summary_df.to_dict(orient='records')
            
        except Exception as e:
            print(f"Ocorreu um erro durante a busca de dados do CNES: {e}")
            return None