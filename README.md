# API e Dashboard de Análise de Dados Públicos

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103%2B-blue?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27%2B-blue?logo=streamlit&logoColor=white)


Este repositório contém o projeto completo para a consulta, análise e visualização de dados públicos de saúde e geografia do Brasil, desenvolvido para a Bolsa BIA UPE - 2025 por Henrique Dias.

O projeto é dividido em dois componentes principais:
1.  **Backend (API RESTful):** Uma API robusta em **Python/FastAPI** que integra e processa dados de fontes como DATASUS (PySUS) e IBGE (SidraPy).
2.  **Frontend (Dashboard Interativo):** Uma aplicação em **Streamlit** que consome a API para fornecer uma interface amigável para consultas e geração de mapas temáticos.



##  Funcionalidades Principais

* **Backend Robusto:**
    * **Integração com PySUS:** Acesso otimizado para grandes volumes de dados de sistemas como `SINAN`, `SIM`, `SINASC`, `SIH`, `SIA` e `CNES`.
    * **Integração com Sidra/IBGE:** Consulta parametrizada de tabelas e metadados.
    * **Geração de Mapas Temáticos:** Endpoint dedicado para criar mapas coropléticos (ex: taxa de natalidade por município) sob demanda.
    * **Arquitetura Limpa e Escalável:** Separação clara entre lógica de negócio (`domain`) e frameworks (`infrastructure`).
    * **Processamento Assíncrono:** Garante que a API permaneça responsiva mesmo durante tarefas pesadas.

* **Frontend Interativo:**
    * **Consultas Dinâmicas:** Interface para explorar dados demográficos e econômicos do IBGE.
    * **Gerador de Mapas:** Formulário para selecionar estado, ano e métrica e visualizar mapas geográficos.
    * **Navegador de Sistemas de Saúde:** Ferramenta para consultar dados de agravos e doenças do DATASUS.

## 🛠️ Tecnologias Utilizadas

| Componente      | Tecnologia/Biblioteca                                        |
| :-------------- | :----------------------------------------------------------- |
| **Backend** | Python 3.12+, FastAPI, Uvicorn                               |
| **Frontend** | Streamlit, Requests                                          |
| **Dados** | pandas, geopandas, pysus, sidrapy, geobr, pyarrow            |
| **Visualização**| matplotlib                                                   |

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.10 ou superior
* Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/upe-campus-surubim/spatial-analysis-algorithms.git
cd spatial-analysis-algorithms
```

### 2. Configurar e Rodar o Backend

O backend é a fonte de dados para o frontend e deve ser executado primeiro.

```bash
# Navegue até a pasta do backend
cd backend/

# Crie e ative um ambiente virtual
python -m venv venv_backend
source venv_backend/bin/activate  # Linux/macOS
# .\venv_backend\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor da API
uvicorn main:app --reload

```

### 3. Configurar e Rodar o Frontend
```bash

# Navegue até a pasta do frontend (a partir da raiz do projeto)
cd frontend/

# (Opcional, mas recomendado) Crie e ative um ambiente virtual
python -m venv venv_frontend
source venv_frontend/bin/activate  # Linux/macOS
# .\venv_frontend\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie o Streamlit
streamlit run Home.py

```


## Estrutura do Projeto

```bash

├── backend/
│   ├── src/
│   │   ├── domain/         # Lógica de negócio pura (UseCases)
│   │   └── infrastructure/ # Controladores, acesso a dados, etc.
│   ├── main.py             # Ponto de entrada da API FastAPI
│   └── requirements.txt    # Dependências do backend
│
├── frontend/
│   ├── src/                # Módulos da UI do Streamlit
│   ├── Home.py             # Ponto de entrada da aplicação Streamlit
│   └── requirements.txt    # Dependências do frontend
│
└── README.md               # Este arquivo
```
