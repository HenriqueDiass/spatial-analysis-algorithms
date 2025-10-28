# Projetos/app.py
import threading
import uvicorn
import streamlit.web.cli as stcli
import sys
import os 
from pathlib import Path 
import sys
import os

# Garante que o diretório backend/ está no caminho de importação
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

# --- CONFIGURAÇÃO DO CAMINHO PARA IMPORTAÇÕES (AQUI ESTAVA O PROBLEMA) ---
# Adiciona o diretório 'Projetos/' (onde app.py está) ao caminho do Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR)) # Usa insert(0) para garantir que seja o primeiro a ser procurado

# Agora esta importação deve funcionar
from backend.main import app as fastapi_app

def run_api():
    """Roda a API FastAPI em localhost:8000 (acessível internamente pelo Streamlit)."""
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

def run_streamlit():
    """Roda o frontend Streamlit."""
    sys.argv = ["streamlit", "run", "frontend/Home.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    print("🚀 Iniciando o backend FastAPI em 0.0.0.0:8000...")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    print("💻 Iniciando o frontend Streamlit em 0.0.0.0:8501...")
    run_streamlit()