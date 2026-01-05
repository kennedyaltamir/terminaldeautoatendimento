from fastapi.testclient import TestClient
from app.main import app
import pytest
import json

client = TestClient(app)

def test_websocket_driver_location_relay():
    """
    Testa se a localização enviada por um cliente (Motorista)
    é retransmitida para outro cliente (Cliente Final) na mesma empresa.
    """
    slug = "relay-test-corp"
    
    # 1. Cliente Final conecta (Ouvinte)
    with client.websocket_connect(f"/ws/{slug}") as ws_customer:
        
        # 2. Motorista conecta (Emissor)
        with client.websocket_connect(f"/ws/{slug}") as ws_driver:
            
            # 3. Motorista envia localização
            location_payload = {
                "type": "driver_location",
                "order_id": "123",
                "lat": -23.5505,
                "lng": -46.6333
            }
            ws_driver.send_json(location_payload)
            
            # 4. Cliente deve receber a mensagem
            # O receive_json bloqueia até chegar algo
            received = ws_customer.receive_json()
            
            assert received["type"] == "driver_location"
            assert received["order_id"] == "123"
            assert received["lat"] == -23.5505
            
            print("✅ Relay de GPS funcionou: Motorista -> Servidor -> Cliente")

def test_websocket_ping_pong():
    """
    Testa o mecanismo de heartbeat para evitar desconexão por inatividade.
    """
    slug = "ping-test"
    with client.websocket_connect(f"/ws/{slug}") as ws:
        ws.send_json({"type": "ping"})
        response = ws.receive_json()
        assert response["type"] == "pong"
        print("✅ Ping/Pong OK")
