# Projetos/app.py
import threading
import uvicorn
import streamlit.web.cli as stcli
import sys
import os # Novo
from pathlib import Path # Novo

# NOVO: Adicione o diretório pai ('Projetos/') ao path do sistema.
# Isso permite que importações como 'from backend.main import...' e
# 'from backend.src. ...' funcionem corretamente.
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Agora esta importação deve funcionar
from backend.main import app as fastapi_app
def run_api():
    """Roda a API FastAPI em localhost:8000 (acessível internamente pelo Streamlit)."""
    # Importante: O host 0.0.0.0 garante que o servidor escute em todas as interfaces,
    # permitindo que o Streamlit, que está no mesmo ambiente, se comunique.
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

def run_streamlit():
    """Roda o frontend Streamlit."""
    # O Streamlit Cloud vai rodar o 'app.py', mas precisamos dizer ao Streamlit
    # para usar o 'frontend/Home.py' como seu arquivo principal.
    sys.argv = ["streamlit", "run", "frontend/Home.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    # 1. Inicia a API FastAPI em uma thread em segundo plano (daemon=True faz com que a thread
    # seja encerrada se o programa principal - Streamlit - for encerrado).
    print("🚀 Iniciando o backend FastAPI em 0.0.0.0:8000...")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # 2. Inicia o Streamlit no thread principal. O Streamlit Cloud detecta esta execução.
    print("💻 Iniciando o frontend Streamlit em 0.0.0.0:8501...")
    run_streamlit()