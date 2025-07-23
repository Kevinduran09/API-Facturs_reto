import httpx

ORS_API_KEY = "5b3ce3597851110001cf6248b54cedf68940407d8d65cf14afecfec9"
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


async def caltculateDurationAndDistance(origen: tuple[float, float], destino: tuple[float, float]) -> dict:
    latA, lonA = origen
    latB, lonB = destino

    params = {
        "api_key": ORS_API_KEY,
        "start": f"{lonA},{latA}",
        "end": f"{lonB},{latB}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(ORS_URL, params=params)
        data = response.json()

    try:
        segment = data["features"][0]["properties"]["segments"][0]
        distancia_km = segment["distance"] / 1000
        tiempo_estimado_seg = segment["duration"]
        tiempo_estimado_min = round(tiempo_estimado_seg / 60)

        return {
            "distancia_km": distancia_km,
            "tiempo_estimado": tiempo_estimado_min
        }

    except (KeyError, IndexError):
        return {
            "distancia_km": 0,
            "tiempo_estimado": 0
        }
