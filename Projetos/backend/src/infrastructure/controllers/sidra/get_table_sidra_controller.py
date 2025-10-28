from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from backend.src.domain.use_cases.sidra.get_table_sidra_use_case import GetTableSidrapyUseCase

def get_single_table_controller(table_id: int):
    try:
        use_case = GetTableSidrapyUseCase()
        table_metadata = use_case.execute(table_id=table_id)
        if table_metadata is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A tabela com o ID '{table_id}' não foi encontrada.")
        return JSONResponse(content=table_metadata, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro interno no servidor.")