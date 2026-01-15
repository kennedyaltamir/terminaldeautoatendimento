from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_deep_health_check():
    """
    Valida se o endpoint de saúde está monitorando os serviços corretamente.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "database" in data["services"]
    
    # Verifica se o banco retornou 'up'
    assert "up" in data["services"]["database"]
    
    print(f"\n📊 Infra Status: {data['status'].upper()}")
    print(f"🗄️ DB Service: {data['services']['database']}")
    print(f"⚡ Redis Service: {data['services']['redis']}")

def test_api_root_version():
    """Garante que a versão da API foi atualizada para 2.3.1."""
    response = client.get("/")
    assert response.status_code == 200
    assert "2.3.1" in response.json()["message"]
