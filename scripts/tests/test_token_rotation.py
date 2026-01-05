import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
import uuid

client = TestClient(app)

def test_refresh_token_cycle():
    """
    Testa o ciclo de rotação de tokens:
    1. Registro gera Access e Refresh tokens.
    2. Usa o Refresh Token para obter novos tokens.
    3. Valida se o novo Access Token funciona.
    """
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
    assert refresh_token != "dummy" # Agora deve ser um JWT real

    # 2. Refresh (Usando o Header X-Refresh-Token)
    res_refresh = client.post(
        "/api/auth/refresh", 
        headers={"X-Refresh-Token": refresh_token}
    )
    
    assert res_refresh.status_code == 200
    new_tokens = res_refresh.json()
    assert "access_token" in new_tokens
    assert new_tokens["access_token"] != tokens["access_token"]

    # 3. Validar novo token
    headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
    res_me = client.get("/api/admin/company/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["owner_email"] == email

def test_refresh_invalid_token():
    """Garante que tokens lixo são rejeitados pelo refresh."""
    res = client.post(
        "/api/auth/refresh", 
        headers={"X-Refresh-Token": "TOKEN_INVALIDO"}
    )
    assert res.status_code == 401
