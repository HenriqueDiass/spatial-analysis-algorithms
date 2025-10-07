# src/infrastructure/shared/sidra_scraper.py
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

def _parse_sidra_html(html_text: str) -> Optional[Dict[str, Any]]:
    """
    Parses the SIDRA metadata HTML page into a structured dictionary.
    """
    soup = BeautifulSoup(html_text, 'lxml')
    data = {}
    try:
        # --- Informações Gerais ---
        data['tabela_id'] = soup.find('span', id='lblNumeroTabela').text
        data['tabela_nome'] = soup.find('span', id='lblNomeTabela').text
        data['pesquisa'] = soup.find('span', id='lblNomePesquisa').text.strip()
        data['assunto'] = soup.find('span', id='lblNomeAssunto').text.strip()
        data['ultima_atualizacao'] = soup.find('span', id='lblDataAtualizacao').text

        # --- Período ---
        periodo_raw = soup.find('span', id='lblPeriodoDisponibilidade').text.strip()
        data['periodo'] = {
            'id': 'P',
            'nome': soup.find('span', id='lblNomePeriodo').text.strip(),
            'disponibilidade': [p.strip() for p in periodo_raw.split(',')] if ',' in periodo_raw else [periodo_raw]
        }
        
        # --- Variáveis ---
        variaveis_list = []
        variaveis_table = soup.find('span', id='lblVariaveis').find_next('table')
        if variaveis_table:
            for row in variaveis_table.find_all('tr'):
                spans = row.find_all('span')
                if len(spans) >= 2:
                    variaveis_list.append({'id': spans[0].text, 'nome': spans[1].text})
        data['variaveis'] = variaveis_list

        # --- Níveis Territoriais ---
        niveis_list = []
        niveis_table = soup.find('span', id='lblNivelterritorial').find_next('table')
        if niveis_table:
            for row in niveis_table.find_all('tr'):
                id_span = row.select_one("span[id*='lblIdNivelterritorial']")
                nome_span = row.select_one("span[id*='lblNomeNivelterritorial']")
                qtd_span = row.select_one("span[id*='lblQuantidadeUnidadesTerritoriais']")
                if id_span and nome_span and qtd_span:
                    niveis_list.append({'id': 'N' + id_span.text, 'nome': f"{nome_span.text}{qtd_span.text}"})
        data['niveis_territoriais'] = niveis_list

        # --- Notas e Fonte ---
        nota_span = soup.find('span', id='lblTextoDescricao')
        if nota_span:
            data['notas'] = nota_span.get_text(separator='\n').strip()
        
        fonte_span = soup.find('span', id='lblFonte')
        if fonte_span:
            data['fonte'] = fonte_span.text.strip()

        return data
    except Exception as e:
        # Em produção, você usaria um sistema de logging aqui.
        print(f"Erro ao processar o HTML do Sidra: {e}") 
        return None


def get_structured_description(table_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetches and parses the metadata for a given SIDRA table ID.
    """
    url = f"https://apisidra.ibge.gov.br/desctabapi.aspx?c={table_id}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        # Chama a função auxiliar corrigida
        return _parse_sidra_html(response.text)
    except requests.exceptions.RequestException as e:
        # Lembre-se de incluir a variável de exceção no bloco except
        print(f"Erro ao buscar descrição da tabela {table_id}: {e}")
        return None