from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
import uuid

client = TestClient(app)

def test_register_and_login_flow():
    """
    Testa o fluxo completo de autenticação que as novas telas usam.
    1. Registro de nova empresa.
    2. Login com as credenciais criadas.
    3. Verificação do token.
    """
    
    # Dados únicos para evitar conflito com seeds
    unique_slug = f"test-rest-{uuid.uuid4().hex[:6]}"
    unique_email = f"test-{uuid.uuid4().hex[:6]}@email.com"
    password = "securepassword123"
    
    # 1. Registro
    register_payload = {
        "company_name": "Restaurante Teste V2",
        "company_slug": unique_slug,
        "owner_email": unique_email,
        "password": password
    }
    
    reg_res = client.post("/api/auth/register", json=register_payload)
    assert reg_res.status_code == 201
    assert "access_token" in reg_res.json()
    
    # 2. Login
    login_payload = {
        "username": unique_email,
        "password": password
    }
    
    login_res = client.post("/api/auth/token", data=login_payload)
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token is not None
    
    # 3. Acesso Protegido (Verificar se o token funciona)
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/admin/company/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["name"] == "Restaurante Teste V2"