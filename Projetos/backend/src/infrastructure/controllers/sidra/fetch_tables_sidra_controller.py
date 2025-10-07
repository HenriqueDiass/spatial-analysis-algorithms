from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from src.domain.use_cases.sidra.fetch_tables_sidra_use_case import FetchTablesSidrapyUseCase

def fetch_all_tables_controller():
    try:
        use_case = FetchTablesSidrapyUseCase()
        tables_list = use_case.execute()
        if tables_list is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="O serviço do IBGE/SIDRA está indisponível.")
        return JSONResponse(content=tables_list, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro interno no servidor.")