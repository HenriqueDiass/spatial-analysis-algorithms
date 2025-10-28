import requests
import pandas as pd

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
API_TIMEOUT = 30

def _get_request(url: str):
    """Função auxiliar para fazer requisições GET com tratamento de erro padronizado."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=API_TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\nERRO DE API na URL {url}: {e}")
        return None

def get_estados():
    """Busca todos os estados do Brasil e retorna como DataFrame."""
    data = _get_request("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    if data:
        df = pd.DataFrame(data)[['id', 'sigla', 'nome']]
        df['id'] = df['id'].astype(str)
        return df
    return None

def get_municipios_por_estado(sigla_uf: str):
    """Busca os municípios de um estado e retorna como DataFrame."""
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla_uf}/municipios"
    data = _get_request(url)
    if data:
        df = pd.DataFrame(data)[['id', 'nome']]
        df['id'] = df['id'].astype(str)
        return df
    return None

def get_regioes_por_estado(id_estado: str, tipo_regiao: str):
    """Busca regiões imediatas ou intermediárias de um estado e retorna como DataFrame."""
    # tipo_regiao pode ser 'regioes-imediatas' ou 'regioes-intermediarias'
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{id_estado}/{tipo_regiao}"
    data = _get_request(url)
    if data:
        df = pd.DataFrame(data)[['id', 'nome']]
        df['id'] = df['id'].astype(str)
        return df
    return None

def get_malha_geojson(tipo_localidade: str, id_localidade: str):
    """Obtém a malha GeoJSON para qualquer tipo de localidade."""
    # tipo_localidade: 'estados', 'municipios', 'regioes-imediatas', 'regioes-intermediarias'
    base_url = "https://servicodados.ibge.gov.br/api/v2/malhas"
    if tipo_localidade.startswith("regioes"):
         base_url = "https://servicodados.ibge.gov.br/api/v4/malhas" # API v4 para regiões
         return _get_request(f"{base_url}/{tipo_localidade}/{id_localidade}?formato=application/vnd.geo+json")
    
    return _get_request(f"{base_url}/{id_localidade}?formato=application/vnd.geo+json")

def get_populacao(nivel_localidade: str, id_localidade: str):
    """Obtém a população para um dado nível (N3=estado, N6=municipio) e ID."""
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021/variaveis/9324?localidades={nivel_localidade}[{id_localidade}]"
    data = _get_request(url)
    try:
        if data and 'resultados' in data[0] and data[0]['resultados']:
            pop_str = data[0]['resultados'][0]['series'][0]['serie']['2021']
            return int(pop_str)
        return None
    except (IndexError, KeyError, TypeError):
        return None