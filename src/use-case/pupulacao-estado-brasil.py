import requests
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def listar_estados():
    """Lista todos os estados brasileiros."""
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        estados = response.json()
        return sorted(estados, key=lambda e: e['sigla'])
    except requests.exceptions.RequestException as e:
        print(f"-> ERRO ao buscar lista de estados: {e}")
        return None

def obter_populacao_estado(codigo_uf: str):
    """Obtém a população de um estado específico para o ano de 2021."""
    # O agregado 6579 é 'População residente', variável 9324 é 'População'.
    # Estamos buscando por 'N3' que representa as Unidades da Federação (Estados).
    url = (
        f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021/variaveis/9324"
        f"?localidades=N3[{codigo_uf}]"
    )
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        dados = response.json()
        if dados and dados[0]['resultados'][0]['series'][0]['serie']['2021']:
            pop_str = dados[0]['resultados'][0]['series'][0]['serie']['2021']
            return int(pop_str)
        return None
    except (requests.exceptions.RequestException, IndexError, KeyError) as e:
        print(f"-> AVISO: Não foi possível obter a população para o estado {codigo_uf}. Erro: {e}")
        return None

if __name__ == "__main__":
    estados = listar_estados()
    if estados is None:
        print("Não foi possível obter a lista de estados. Encerrando.")
        exit()

    estados_com_populacao = []

    print("Iniciando o processamento de dados de população para todos os estados do Brasil...\n")

    for estado in estados:
        codigo_uf = str(estado['id'])
        nome_estado = estado['nome']
        sigla_uf = estado['sigla']

        print(f"Processando população do estado: {nome_estado} ({sigla_uf})...")

        populacao_estado = obter_populacao_estado(codigo_uf)

        if populacao_estado is not None:
            print(f"  População de {nome_estado}: {populacao_estado:,.0f}")
        else:
            populacao_estado = 0 # Define como 0 se a população não for encontrada
            print(f"  População de {nome_estado}: NÃO ENCONTRADA")

        estados_com_populacao.append({
            "estado": nome_estado,
            "sigla": sigla_uf,
            "codigoIBGE": codigo_uf,
            "populacao_2021": populacao_estado
        })
        time.sleep(0.1) # Pequeno atraso para evitar sobrecarregar a API

    # Salvar resultados em JSON
    output_filename = "populacao-estados-brasil.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(estados_com_populacao, f, ensure_ascii=False, indent=2)

    print("\n" + "="*80)
    print("Processamento de dados de população dos estados concluído.")
    print(f"Dados salvos em '{output_filename}'.")
    print("="*80)