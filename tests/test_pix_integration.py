from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_pix_key():
    """Valida se o admin consegue salvar sua chave PIX"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Update PIX
    payload = {
        "pix_key": "financeiro@mesaflow.com"
    }
    response = client.patch("/api/admin/company/me", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["pix_key"] == "financeiro@mesaflow.com"

def test_menu_returns_pix_key():
    """Garante que a chave PIX é enviada para o cardápio público"""
    response = client.get("/api/hamburgueria-ze/menu")
    assert response.status_code == 200
    assert "pix_key" in response.json()["company"]