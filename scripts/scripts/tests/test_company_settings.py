from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_company_hours():
    """Valida se o sistema aceita a atualização de horários de funcionamento"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Update Hours
    payload = {
        "opens_at": "09:00:00",
        "closes_at": "23:00:00"
    }
    response = client.patch("/api/admin/company/me", headers=headers, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["opens_at"] == "09:00:00"
    assert data["closes_at"] == "23:00:00"