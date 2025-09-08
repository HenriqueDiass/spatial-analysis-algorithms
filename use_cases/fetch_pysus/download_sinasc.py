# use_cases/fetch_pysus/download_sinasc.py

import pandas as pd
from pysus import SINASC
from typing import List, Optional, Tuple
from shared import pysus_tools

def execute(group_code: str, years: List[int], states: Optional[List[str]] = None) -> Tuple[pd.DataFrame, dict]:
    """
    Busca dados do SINASC e calcula nascimentos por município, sexo e faixa etária da mãe.
    Agora é robusto para lidar com o retorno da função download() sendo uma lista.
    """
    try:
        print(f"➡️  Iniciando busca no SINASC para o grupo '{group_code}'...")
        sinasc = SINASC().load()
        # Otimização: Tenta buscar arquivos apenas para o(s) estado(s) selecionado(s)
        files_to_download = sinasc.get_files(group=group_code, year=years, uf=states)
        if not files_to_download:
            print("⚠️  Nenhum arquivo encontrado."); return pd.DataFrame(), {}
            
        print(f"📂 {len(files_to_download)} arquivo(s) encontrado(s). Baixando...")
        downloaded_objects = sinasc.download(files_to_download)
        
        print("🔄  Processando para DataFrame...")
        # Verifica se o resultado é uma lista de objetos ou um único DataSet
        if isinstance(downloaded_objects, list):
            # Se for uma lista, converte cada item e depois concatena
            list_of_dataframes = [pq.to_dataframe() for pq in downloaded_objects]
            unfiltered_df = pd.concat(list_of_dataframes, ignore_index=True) if list_of_dataframes else pd.DataFrame()
        else:
            # Se não for uma lista, assume que o objeto tem o método .to_dataframe()
            unfiltered_df = downloaded_objects.to_dataframe()
        

        # A filtragem manual continua como uma garantia
        filtered_df = pysus_tools.filter_dataframe_by_states(unfiltered_df, states, 'CODMUNNASC')
        
        print("➕  Adicionando coluna de faixa etária e calculando nascimentos por município...")
        cases_per_municipality = {}
        # Garante que as colunas necessárias para o cálculo existem
        required_cols = ['IDADEMAE', 'CODMUNNASC', 'SEXO']
        if all(col in filtered_df.columns for col in required_cols):
            df_processed = filtered_df.dropna(subset=required_cols).copy()
            # A coluna 'MotherAgeGroup' agora é criada apenas no df_processed
            df_processed['MotherAgeGroup'] = df_processed['IDADEMAE'].apply(pysus_tools.get_age_group)
            
            summary = df_processed.groupby(['CODMUNNASC', 'SEXO', 'MotherAgeGroup']).size().reset_index(name='quantidade')
            
            for _, row in summary.iterrows():
                mun, sexo, faixa, qtde = str(row['CODMUNNASC']), str(row['SEXO']), str(row['MotherAgeGroup']), int(row['quantidade'])
                if mun not in cases_per_municipality:
                    cases_per_municipality[mun] = {"total": 0, "by_sexo": {}, "by_faixa_etaria_mae": {}}
                cases_per_municipality[mun]["total"] += qtde
                cases_per_municipality[mun]["by_sexo"][sexo] = cases_per_municipality[mun]["by_sexo"].get(sexo, 0) + qtde
                cases_per_municipality[mun]["by_faixa_etaria_mae"][faixa] = cases_per_municipality[mun]["by_faixa_etaria_mae"].get(faixa, 0) + qtde
            print("✅  Cálculos concluídos.")
        else:
            df_processed = filtered_df
            print("ℹ️  Não foi possível calcular os nascimentos por município (colunas não encontradas).")

        print(f"✅  Processo concluído! {len(df_processed)} registros foram carregados.")
        return df_processed, cases_per_municipality
    except Exception as e:
        print(f"❌  Ocorreu um erro durante a busca no SINASC: {e}")
        return pd.DataFrame(), {}