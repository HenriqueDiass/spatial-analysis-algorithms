# use_cases/fetch_states/index.py

import time
from shared.ibge_api import get_estados, get_malha_geojson, get_populacao
from shared.file_utils import save_geojson

class FetchStatesUseCase:
    """
    Caso de Uso que busca dados detalhados (malha, população)
    de todos os estados do Brasil e salva o resultado em um arquivo GeoJSON.
    """
    
    def execute(self, output_filename: str):
        """
        Executa o caso de uso.

        :param output_filename: O nome do arquivo GeoJSON de saída.
        """
        estados_df = get_estados()
        if estados_df is None:
            print("Não foi possível obter a lista de estados. Abortando.")
            return

        features = []
        print("\n--- Iniciando coleta: DADOS COMPLETOS POR ESTADO ---")
        for _, estado in estados_df.iterrows():
            id_uf, sigla, nome = estado['id'], estado['sigla'], estado['nome']
            print(f"Processando {nome} ({sigla})... ", end="", flush=True)
            
            malha = get_malha_geojson("estados", id_uf)
            populacao_valor = get_populacao("N3", id_uf)

            if malha and 'features' in malha and malha['features']:
                feature = malha['features'][0]
                feature['properties']['sigla'] = sigla
                feature['properties']['nome'] = nome
                
                # --- CÓDIGO CORRIGIDO ---
                # Lógica de conversão segura para a população
                try:
                    # Tenta converter o valor para inteiro. Funciona para ints (ex: 5) e strings (ex: "5").
                    feature['properties']['populacao_2021'] = int(populacao_valor)
                except (ValueError, TypeError):
                    # Se a conversão falhar (ex: valor é None ou uma string vazia), usa 0.
                    feature['properties']['populacao_2021'] = 0
                
                features.append(feature)
                print("OK")
            else:
                print("FALHA na malha")
            time.sleep(0.1)

        save_geojson(features, output_filename)
        print(f"\n✅ Processo finalizado. Arquivo salvo em: {output_filename}")