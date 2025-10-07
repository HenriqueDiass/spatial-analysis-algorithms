# src/infrastructure/controllers/maps/get_map_birthrate_controller.py

from fastapi import HTTPException
# Importação explícita do Response necessário para retornar imagens
from fastapi.responses import Response # <-- Usamos Response, que é mais comum para buffers fixos como PNG
from src.domain.use_cases.maps.get_map_birthrate_use_case import GetMapBirthrateUseCase

# Adicionamos 'group_code' como um novo parâmetro
def generate_birth_rate_map(state_abbr: str, year: int, metric: str, group_code: str):
    """
    Controller que orquestra a geração do mapa coroplético de natalidade.
    """
    try:
        use_case = GetMapBirthrateUseCase()
        
        # O UseCase retorna um io.BytesIO (buffer)
        image_buffer = use_case.execute(
            state_abbr=state_abbr,
            year=year,
            metric_column=metric,
            group_code=group_code
        )

        if image_buffer is None:
            raise HTTPException(
                status_code=404, 
                detail=f"Não foi possível gerar o mapa. Dados não encontrados para a combinação: {state_abbr}/{year}."
            )
        
        # Retorna o buffer como uma imagem PNG
        # O Streamlit lida bem com o content/media_type "image/png"
        return Response(content=image_buffer.read(), media_type="image/png")

    except Exception as e:
        # Lança a exceção para que o FastAPI capture e retorne o erro 500
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno no servidor: {e}")