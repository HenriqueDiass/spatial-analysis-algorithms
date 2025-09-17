import pandas as pd
import sidrapy
import os
from typing import Optional, Dict

# Dicionário para mapear a sigla do estado para o código IBGE
STATE_ABBR_TO_IBGE_CODE: Dict[str, str] = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14", "PA": "15", "AP": "16", "TO": "17",
    "MA": "21", "PI": "22", "CE": "23", "RN": "24", "PB": "25", "PE": "26", "AL": "27",
    "SE": "28", "BA": "29", "MG": "31", "ES": "32", "RJ": "33", "SP": "35",
    "PR": "41", "SC": "42", "RS": "43", "MS": "50", "MT": "51", "GO": "52", "DF": "53"
}

def execute(
    year: int, 
    state_abbr: str, 
    output_dir: str
) -> bool:
    """
    Busca dados de população do Sidra/IBGE para todos os municípios de um estado
    e salva o resultado em um arquivo JSON.
    
    Esta função seleciona automaticamente a tabela correta do IBGE
    (Censo de 2022 ou Estimativas para outros anos).
    """
    print(f"\n▶️  Iniciando busca de população no IBGE/Sidra para {state_abbr.upper()} - {year}...")
    
    state_abbr = state_abbr.upper()
    if state_abbr not in STATE_ABBR_TO_IBGE_CODE:
        print(f"❌ ERRO: A sigla '{state_abbr}' não é um estado válido.")
        return False
    
    ibge_state_code = STATE_ABBR_TO_IBGE_CODE[state_abbr]

    if year == 2022:
        table_to_use = "4709"
        variable_to_use = "93"
        print("   -> Ano do Censo (2022) detectado. Usando tabela 4709.")
    else:
        table_to_use = "6579"
        variable_to_use = "9324"
        print(f"   -> Ano de Estimativa ({year}) detectado. Usando tabela 6579.")

    try:
        codigo_territorial_formatado = f"in n3 {ibge_state_code}"
        
        print(f"   -> Conectando à API... (Tabela: {table_to_use}, Variável: {variable_to_use})")
        raw_data = sidrapy.get_table(
            table_code=table_to_use,
            territorial_level="6",
            ibge_territorial_code=codigo_territorial_formatado,
            variable=variable_to_use,
            period=str(year),
            header="y"
        )
        print("   -> Dados brutos recebidos com sucesso.")
        
    except Exception as e:
        print(f"❌ ERRO: Falha durante a busca de dados na API do Sidra. Detalhes: {e}")
        return False
        
    if raw_data is None or len(raw_data) <= 1:
        print(f"⚠️  AVISO: Nenhum dado de população encontrado para {state_abbr} em {year}.")
        return False
        
    print("   -> Processando e limpando os dados...")
    
    df = raw_data.copy()
    df.columns = df.iloc[0]
    df = df.drop(0).reset_index(drop=True)

    df.rename(columns={
        'Município (Código)': 'code_muni_7digit',
        'Município': 'municipality_name',
        'Valor': 'population'
    }, inplace=True)

    required_cols = ['code_muni_7digit', 'municipality_name', 'population']
    if not all(col in df.columns for col in required_cols):
        print("❌ ERRO: Colunas esperadas não encontradas no retorno da API.")
        print(f"   -> Colunas disponíveis: {df.columns.tolist()}")
        return False

    final_df = df[required_cols].copy()
    final_df['code_muni_7digit'] = pd.to_numeric(final_df['code_muni_7digit'], errors='coerce')
    final_df['population'] = pd.to_numeric(final_df['population'], errors='coerce')
    final_df.dropna(inplace=True)
    final_df = final_df.astype({'code_muni_7digit': int, 'population': int})
    final_df['code_muni_6digit'] = final_df['code_muni_7digit'] // 10
    
    final_df = final_df[['code_muni_6digit', 'code_muni_7digit', 'municipality_name', 'population']]
    
    try:
        # --- LINHA ALTERADA ---
        # O nome do arquivo agora está fixo no padrão que você pediu.
        output_filename = f"ibge_population_{state_abbr}_{year}_censo.json"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"   -> Salvando dados em formato JSON...")
        final_df.to_json(
            output_path, orient='records', indent=4, force_ascii=False
        )
        print(f"✅ Arquivo de população salvo com sucesso em: {output_path}")
        return True
    except Exception as e:
        print(f"❌ ERRO ao salvar o arquivo JSON: {e}")
        return False