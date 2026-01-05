import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
import time

client = TestClient(app)

def test_refresh_token_cycle():
    unique_id = uuid.uuid4().hex[:6]
    email = f"session-{unique_id}@test.com"

    # 1. Registro
    reg_payload = {
        "company_name": "Session Corp",
        "company_slug": f"session-{unique_id}",
        "owner_email": email,
        "password": "Password123!"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code == 201
    tokens = res_reg.json()

    refresh_token = tokens["refresh_token"]

    # Pequeno delay para garantir que o timestamp do novo token seja diferente
    time.sleep(1)

    # 2. Refresh
    res_refresh = client.post(
        "/api/auth/refresh",
        headers={"X-Refresh-Token": refresh_token}
    )

    assert res_refresh.status_code == 200
    new_tokens = res_refresh.json()
    
    # O token de acesso deve mudar
    assert new_tokens["access_token"] != tokens["access_token"]
