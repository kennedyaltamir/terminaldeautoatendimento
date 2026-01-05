from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_password_update_flow():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Tentar mudar senha com senha atual errada
    wrong_payload = {"current_password": "senha_errada_123", "new_password": "newpassword123"}
    response = client.patch("/api/admin/company/me/password", headers=headers, json=wrong_payload)
    assert response.status_code == 400
    # Mensagem flexível
    assert "incorreta" in response.json()["detail"].lower()
