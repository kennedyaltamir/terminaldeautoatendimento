from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_metrics_access():
    """Valida se a rota de métricas retorna dados estruturados corretamente"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Metrics
    response = client.get("/api/admin/metrics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    
    # 3. Validar campos obrigatórios
    assert "total_revenue" in data
    assert "total_orders" in data
    assert "average_ticket" in data
    assert "top_products" in data
    assert isinstance(data["top_products"], list)