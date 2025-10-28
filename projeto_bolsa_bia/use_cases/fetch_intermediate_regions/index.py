import time
from shared.ibge_api import get_estados, get_regioes_por_estado, get_malha_geojson
from shared.file_utils import save_geojson

class FetchIntermediateRegionsUseCase:
    """
    Caso de Uso que orquestra a busca de dados de todas as regiões
    intermediárias do Brasil e salva o resultado em um arquivo GeoJSON.
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
        print("\n--- Iniciando coleta: REGIÕES INTERMEDIÁRIAS DO BRASIL ---")
        for _, estado in estados_df.iterrows():
            print(f"Processando estado: {estado['sigla']}")
            # A string aqui foi ajustada para o endpoint correto
            regioes_df = get_regioes_por_estado(estado['id'], 'regioes-intermediarias')
            if regioes_df is None: continue

            for _, regiao in regioes_df.iterrows():
                id_regiao, nome_regiao = regiao['id'], regiao['nome']
                print(f"  Obtendo malha de {nome_regiao}... ", end="", flush=True)
                # E aqui também
                malha = get_malha_geojson('regioes-intermediarias', id_regiao)

                if malha and 'features' in malha and malha['features']:
                    feature = malha['features'][0]
                    # As propriedades também foram ajustadas
                    feature['properties']['id_regiao_intermediaria'] = id_regiao
                    feature['properties']['nome_regiao_intermediaria'] = nome_regiao
                    feature['properties']['uf_sigla'] = estado['sigla']
                    features.append(feature)
                    print("OK")
                else:
                    print("FALHA na malha")
                time.sleep(0.1)
        
        save_geojson(features, output_filename)
        print(f"\n✅ Processo finalizado. Arquivo salvo em: {output_filename}")