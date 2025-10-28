# use_cases/fetch_municipalities/index.py

import time
from shared.ibge_api import get_municipios_por_estado, get_malha_geojson, get_populacao
from shared.file_utils import save_geojson

class FetchMunicipalitiesUseCase:
    """
    Caso de Uso que busca dados detalhados (malha, população)
    dos municípios de um determinado estado da federação.
    """

    def execute(self, sigla_uf: str, output_filename: str):
        """
        Executa a busca de dados para os municípios de um estado.

        :param sigla_uf: A sigla do estado a ser processado (ex: 'PE').
        :param output_filename: O nome do arquivo GeoJSON de saída.
        """
        municipios_df = get_municipios_por_estado(sigla_uf)
        if municipios_df is None:
            print(f"Não foi possível obter a lista de municípios para {sigla_uf}.")
            return

        features = []
        print(f"\n--- Iniciando coleta: DADOS DOS MUNICÍPIOS DE {sigla_uf.upper()} ---")
        for _, municipio in municipios_df.iterrows():
            id_municipio, nome = municipio['id'], municipio['nome']
            print(f"  Processando {nome} ({id_municipio})... ", end="", flush=True)
            
            malha = get_malha_geojson("municipios", id_municipio)
            populacao_valor = get_populacao("N6", id_municipio)

            if malha and 'features' in malha and malha['features']:
                feature = malha['features'][0]
                feature["properties"]["name"] = nome
                
                # --- CÓDIGO CORRIGIDO ---
                # Mesma lógica de conversão segura para a população
                try:
                    feature["properties"]["populacao"] = int(populacao_valor)
                except (ValueError, TypeError):
                    feature["properties"]["populacao"] = 0
                    
                features.append(feature)
                print("OK")
            else:
                print("FALHA na malha")
            time.sleep(0.1)
        
        save_geojson(features, output_filename)
        print(f"\n✅ Processo finalizado. Arquivo salvo em: {output_filename}")