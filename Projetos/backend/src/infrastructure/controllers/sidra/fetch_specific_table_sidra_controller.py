from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from src.domain.use_cases.sidra.fetch_specific_table_sidra_use_case import FetchSpecificTableSidraUseCase


def fetch_specific_table_controller(params: dict):
    try:
        use_case = FetchSpecificTableSidraUseCase()
        result = use_case.execute(params)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum dado encontrado para os parâmetros informados."
            )

        return JSONResponse(content=result, status_code=status.HTTP_200_OK)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao consultar dados no SIDRA."
        )
