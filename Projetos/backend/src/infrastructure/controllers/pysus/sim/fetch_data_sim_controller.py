# src/infrastructure/controllers/pysus/sim/fetch_data_sim_controller.py

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from typing import List, Optional

# --- IMPORTAÇÃO CHAVE ---
from fastapi.concurrency import run_in_threadpool 

from backend.src.domain.use_cases.pysus.sim.fetch_data_sim_use_case import FetchDataSimUseCase

# O controller é async def, como o do SINAN
async def fetch_sim_data_controller(group_code: str, years: List[int], states: Optional[List[str]]):
    """
    Controller que busca um resumo de dados do SIM de forma não-bloqueante (assíncrona).
    """
    try:
        if not years:
            raise HTTPException(status_code=400, detail="O parâmetro 'years' é obrigatório.")

        params = {
            "group_code": group_code.upper(),
            "years": years,
            "states": [st.upper() for st in states] if states else None 
        }

        use_case = FetchDataSimUseCase()

        # --- CHAVE DE CORREÇÃO ---
        # AQUI usamos AWAIT run_in_threadpool para executar o Use Case SÍNCRONO em background
        result_dict = await run_in_threadpool(use_case.execute, **params)
        
        summary_list = result_dict.get("summary_by_municipality", [])

        if summary_list:
            summary_response = {
                "metadata": {
                    "system": "SIM",
                    "parameters": params,
                    # Calcula o total de óbitos
                    "total_records_found": sum(item["total_deaths"] for item in summary_list) 
                },
                "summary_by_municipality": summary_list
            }
            return JSONResponse(content=summary_response, status_code=status.HTTP_200_OK)
        else:
            # Retorna 404 quando o Use Case retorna uma lista vazia (sem dados)
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os parâmetros fornecidos.")

    except HTTPException as http_exc:
        # Repassa exceções HTTP esperadas
        raise http_exc

    except Exception as e:
        # Tratamento robusto para falhas internas
        print(f"Erro interno ao buscar dados do SIM: {e}")
        # Loga o erro, mas retorna 500
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno no servidor.")