from typing import List, Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Mapeia slug da empresa -> Lista de conexões ativas
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, company_slug: str):
        await websocket.accept()
        if company_slug not in self.active_connections:
            self.active_connections[company_slug] = []
        self.active_connections[company_slug].append(websocket)
        print(f"🔌 Nova conexão WS em: {company_slug}. Total: {len(self.active_connections[company_slug])}")

    def disconnect(self, websocket: WebSocket, company_slug: str):
        if company_slug in self.active_connections:
            if websocket in self.active_connections[company_slug]:
                self.active_connections[company_slug].remove(websocket)
                print(f"🔌 Desconexão WS em: {company_slug}")

    async def broadcast(self, message: dict, company_slug: str):
        """Envia mensagem para todos conectados naquele restaurante"""
        if company_slug in self.active_connections:
            # Copia a lista para evitar erro de modificação durante iteração
            connections = self.active_connections[company_slug][:]
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    # Se falhar ao enviar, assume que caiu e remove
                    self.disconnect(connection, company_slug)

manager = ConnectionManager()