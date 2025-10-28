import time
from shared.ibge_api import get_estados, get_regioes_por_estado, get_malha_geojson
from shared.file_utils import save_geojson

class FetchImmediateRegionsUseCase:
    """
    Caso de Uso que orquestra a busca de dados de todas as regiões
    imediatas do Brasil e salva o resultado em um arquivo GeoJSON.
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
        print("\n--- Iniciando coleta: REGIÕES IMEDIATAS DO BRASIL ---")
        for _, estado in estados_df.iterrows():
            print(f"Processando estado: {estado['sigla']}")
            regioes_df = get_regioes_por_estado(estado['id'], 'regioes-imediatas')
            if regioes_df is None: continue

            for _, regiao in regioes_df.iterrows():
                id_regiao, nome_regiao = regiao['id'], regiao['nome']
                print(f"  Obtendo malha de {nome_regiao}... ", end="", flush=True)
                malha = get_malha_geojson('regioes-imediatas', id_regiao)

                if malha and 'features' in malha and malha['features']:
                    feature = malha['features'][0]
                    # Adiciona propriedades ao GeoJSON
                    feature['properties']['id_regiao_imediata'] = id_regiao
                    feature['properties']['nome_regiao_imediata'] = nome_regiao
                    feature['properties']['uf_sigla'] = estado['sigla']
                    features.append(feature)
                    print("OK")
                else:
                    print("FALHA na malha")
                time.sleep(0.1)
        
        # O nome do arquivo agora é um parâmetro, tornando a função reutilizável!
        save_geojson(features, output_filename)
        print(f"\n✅ Processo finalizado. Arquivo salvo em: {output_filename}")
