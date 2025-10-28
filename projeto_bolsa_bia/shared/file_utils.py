# shared/file_utils.py

import json

def save_geojson(features: list, output_filename: str):
    """
    Cria um objeto FeatureCollection e salva em um arquivo .geojson.
    """
    if not output_filename.endswith(".geojson"):
        output_filename += ".geojson"

    geojson_final = {
        "type": "FeatureCollection",
        "features": features
    }

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(geojson_final, f, ensure_ascii=False, indent=2)
        print(f"\nArquivo '{output_filename}' salvo com sucesso!")
        print(f"Total de features salvas: {len(features)}")
    except IOError as e:
        print(f"\nErro ao salvar o arquivo '{output_filename}': {e}")