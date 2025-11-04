from fastapi import HTTPException
from fastapi.responses import Response 
from typing import Optional

# Importar o UseCase que foi modificado/criado
# Assumindo que a classe GetMapStateLayersUseCase está em src/domain/use_cases/maps/get_map_state_layers_use_case.py
from src.domain.use_cases.maps.get_map_state_layers_use_case import GetMapStateLayersUseCase

# O controller agora lida com todos os parâmetros que o UseCase.execute exige, incluindo use_zoom.
def generate_state_layers_map(
    state_abbr: str,
    year: int,
    show_municipalities: Optional[bool] = False, # Define False como padrão, mas permite ser True
    show_immediate: Optional[bool] = False,
    show_intermediate: Optional[bool] = False,
    use_zoom: Optional[bool] = False, 
):
    """
    Controller que orquestra a geração do mapa de divisões regionais de um estado.

    Os parâmetros 'show_*' definem quais camadas serão plotadas.
    O parâmetro 'use_zoom' controla se o mapa foca no estado ou mostra o Brasil.
    """
    print(f"--- [Controller] Recebida solicitação para mapa de camadas de {state_abbr.upper()} ({year}) ---")
    
    try:
        use_case = GetMapStateLayersUseCase()
        
        # O UseCase retorna um io.BytesIO (buffer)
        image_buffer = use_case.execute(
            state_abbr=state_abbr,
            year=year,
            show_municipalities=show_municipalities,
            show_immediate=show_immediate,
            show_intermediate=show_intermediate,
            use_zoom=use_zoom, 
        )

        if image_buffer is None:
            # Esta exceção será lançada se o UseCase não puder gerar a imagem
            raise HTTPException(
                status_code=404, 
                detail=f"Não foi possível gerar o mapa. Dados do estado/ano não encontrados: {state_abbr}/{year}."
            )
        
        # Retorna o buffer como uma imagem PNG
        print("--- [Controller] Retornando imagem PNG ---")
        return Response(content=image_buffer.read(), media_type="image/png")

    except HTTPException as h_e:
        # Repassa a exceção HTTPException (como o 404)
        raise h_e
        
    except Exception as e:
        # Captura qualquer outro erro inesperado e retorna 500
        print(f"❌ ERRO INTERNO no controller: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Ocorreu um erro interno no servidor ao gerar o mapa: {e}"
        )