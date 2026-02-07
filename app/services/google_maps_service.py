# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 02:58:00
import httpx
import os
import logging

logger = logging.getLogger("GoogleMapsService")

class GoogleMapsService:
    @staticmethod
    async def get_route(origin_lat, origin_lng, dest_lat, dest_lng):
        # 🛡️ IMPORTANTE: Esta chave deve estar no seu .env do Backend (raiz)
        api_key = os.getenv("GOOGLE_MAPS_KEY")
        if not api_key:
            logger.error("❌ GOOGLE_MAPS_KEY não configurada no .env")
            return None
            
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": f"{origin_lat},{origin_lng}",
            "destination": f"{dest_lat},{dest_lng}",
            "key": api_key,
            "mode": "driving",
            "region": "br"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.get(url, params=params)
                data = res.json()
                if data.get("status") == "OK":
                    route = data["routes"][0]
                    return {
                        "geometry": route["overview_polyline"]["points"], # Formato Polyline encodado
                        "duration": route["legs"][0]["duration"]["value"],
                        "distance": route["legs"][0]["distance"]["value"]
                    }
                logger.error(f"Google API Error: {data.get('status')} - {data.get('error_message')}")
                return None
            except Exception as e:
                logger.error(f"Falha na conexão com Google: {e}")
                return None
