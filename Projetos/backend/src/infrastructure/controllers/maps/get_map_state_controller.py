from fastapi import HTTPException
from fastapi.responses import Response 
from typing import Optional

from src.domain.use_cases.maps.get_map_state_layers_use_case import GetMapStateLayersUseCase


def generate_state_layers_map(
    state_abbr: str,
    year: int,
    show_municipalities: Optional[bool] = False, 
    show_immediate: Optional[bool] = False,
    show_intermediate: Optional[bool] = False,
    use_zoom: Optional[bool] = False, 
):
    
    print(f"--- [Controller] Recebida solicitação para mapa de camadas de {state_abbr.upper()} ({year}) ---")
    
    try:
        use_case = GetMapStateLayersUseCase()
        
        
        image_buffer = use_case.execute(
            state_abbr=state_abbr,
            year=year,
            show_municipalities=show_municipalities,
            show_immediate=show_immediate,
            show_intermediate=show_intermediate,
            use_zoom=use_zoom, 
        )

        if image_buffer is None:
            raise HTTPException(
                status_code=404, 
                detail=f"Não foi possível gerar o mapa. Dados do estado/ano não encontrados: {state_abbr}/{year}."
            )
        
        print("--- [Controller] Retornando imagem PNG ---")
        return Response(content=image_buffer.read(), media_type="image/png")

    except HTTPException as h_e:
       
        raise h_e
        
    except Exception as e:
        
        print(f"❌ ERRO INTERNO no controller: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Ocorreu um erro interno no servidor ao gerar o mapa: {e}"
        )