import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

# MÓDULO 1: O PARSER DE HTML (Movido para o cliente)
def _parse_sidra_html(html_text: str) -> Optional[Dict[str, Any]]:
    """
    Recebe o texto HTML da página do SIDRA e o transforma em um
    dicionário Python estruturado.
    Função interna, não destinada a ser importada diretamente.
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
        periodo_disponibilidade_raw = soup.find('span', id='lblPeriodoDisponibilidade').text.strip()
        if ',' in periodo_disponibilidade_raw:
            periodo_disponibilidade = [p.strip() for p in periodo_disponibilidade_raw.split(',')]
        else:
            periodo_disponibilidade = periodo_disponibilidade_raw
        data['periodo'] = {
            'id': 'P',
            'nome': soup.find('span', id='lblNomePeriodo').text.strip(),
            'disponibilidade': periodo_disponibilidade
        }

        # --- Variáveis ---
        variaveis_list = []
        variaveis_table = soup.find('span', id='lblVariaveis').find_next('table')
        for row in variaveis_table.find_all('tr'):
            var_id = row.find('span', id=lambda x: x and x.startswith('lstVariaveis_lblIdVariavel_')).text
            var_nome = row.find('span', id=lambda x: x and x.startswith('lstVariaveis_lblNomeVariavel_')).text
            variaveis_list.append({'id': var_id, 'nome': var_nome})
        data['variaveis'] = variaveis_list

        # --- Classificações (se existirem) ---
        classificacoes_list = []
        class_containers = soup.find_all('span', id=lambda x: x and x.startswith('lstClassificacoes_lblIdClassificacao_'))
        if class_containers:
            for container_span in class_containers:
                container_td = container_span.find_parent('td')
                class_id = 'C' + container_span.text
                class_nome = container_td.find('span', id=lambda x: x and x.startswith('lstClassificacoes_lblClassificacao_')).text.strip()
                categorias_list = []
                categorias_table = container_td.find('table')
                for cat_row in categorias_table.find_all('tr'):
                    cat_id = cat_row.find('span', id=lambda x: x and 'lblIdCategoria' in x).text
                    cat_nome = cat_row.find('span', id=lambda x: x and 'lblNomeCategoria' in x).text
                    categorias_list.append({'id': cat_id, 'nome': cat_nome})
                classificacoes_list.append({
                    'id': class_id,
                    'nome': class_nome,
                    'categorias': categorias_list
                })
            data['classificacoes'] = classificacoes_list

        # --- Níveis Territoriais ---
        niveis_list = []
        niveis_table = soup.find('span', id='lblNivelterritorial').find_next('table')
        if niveis_table:
            for row in niveis_table.find_all('tr'):
                nivel_id_num = row.find('span', id=lambda x: x and x.startswith('lstNiveisTerritoriais_lblIdNivelterritorial_')).text
                nivel_id = 'N' + nivel_id_num
                nivel_nome = row.find('span', id=lambda x: x and x.startswith('lstNiveisTerritoriais_lblNomeNivelterritorial_')).text
                nivel_qtd = row.find('span', id=lambda x: x and x.startswith('lstNiveisTerritoriais_lblQuantidadeUnidadesTerritoriais_')).text
                niveis_list.append({'id': nivel_id, 'nome': f"{nivel_nome}{nivel_qtd}"})
            data['niveis_territoriais'] = niveis_list

        # --- Notas e Fonte ---
        nota_span = soup.find('span', id='lblTextoDescricao')
        if nota_span:
            data['notas'] = nota_span.get_text(separator='\n').strip()
        
        fonte_span = soup.find('span', id='lblFonte')
        if fonte_span:
            data['fonte'] = fonte_span.text.strip()

    except AttributeError as e:
        print(f"❌ Erro ao parsear o HTML. Um elemento esperado não foi encontrado: {e}")
        return None
    return data

# MÓDULO 2: O BUSCADOR DE DADOS (Movido para o cliente e agora é a função pública)
def get_structured_description(table_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca a descrição de uma tabela do SIDRA e retorna
    diretamente como um dicionário Python (JSON) estruturado.
    """
    print(f"Buscando metadados da tabela {table_id}...")
    url = f"https://apisidra.ibge.gov.br/desctabapi.aspx?c={table_id}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        structured_json = _parse_sidra_html(response.text)
        return structured_json
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP ao buscar tabela {table_id}. Tabela pode não existir. ({e})")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão ao buscar tabela {table_id}: {e}")
        return None