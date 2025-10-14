from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional
# --- NOVA IMPORTAÇÃO ---
from fastapi.concurrency import run_in_threadpool

from src.domain.use_cases.pysus.sinan.fetch_data_sinan_use_case import FetchDataSinanUseCase

# A função do controller agora também é 'async def'
async def fetch_sinan_data_controller(disease_code: str, years: List[int], states: Optional[List[str]]):
    """
    Controller que busca um resumo de dados do SINAN de forma não-bloqueante.
    """
    try:
        params = {
            "disease_code": disease_code,
            "years": years,
            "states": states # O UseCase já lida com a conversão para maiúsculas etc.
        }

        use_case = FetchDataSinanUseCase()

        # --- A MÁGICA ACONTECE AQUI ---
        # Em vez de: summary_list = use_case.execute(**params)
        # Nós pedimos para o FastAPI rodar a função pesada 'use_case.execute'
        # em uma thread pool, e esperamos ('await') pelo resultado.
        summary_list = await run_in_threadpool(use_case.execute, **params)
        
        if summary_list:
            summary_response = {
                "metadata": {
                    "system": "SINAN",
                    "parameters": params,
                    "total_records_found": sum(item['total_cases'] for item in summary_list)
                },
                "summary_by_municipality": summary_list
            }
            return JSONResponse(content=summary_response, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado.")

    except Exception as e:
        print(f"Erro interno ao buscar dados do SINAN: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")