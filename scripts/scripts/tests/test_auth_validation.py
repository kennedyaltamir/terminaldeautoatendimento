from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_auth_backend_validation_rules():
    """
    Testa se o backend rejeita dados que o frontend (Zod) também rejeitaria.
    Segurança em profundidade.
    """
    
    unique_slug = f"test-{uuid.uuid4().hex[:6]}"
    
    # 1. Teste Senha Curta
    short_pass_payload = {
        "company_name": "Test Short Pass",
        "company_slug": f"{unique_slug}-short",
        "owner_email": "short@test.com",
        "password": "123" # Muito curta (backend pede min 6 no Schema)
    }
    
    res_short = client.post("/api/auth/register", json=short_pass_payload)
    # O Pydantic valida min_length=6 no SignUpRequest (app/schemas.py)
    assert res_short.status_code == 422
    
    # 2. Teste Email Inválido
    invalid_email_payload = {
        "company_name": "Test Bad Email",
        "company_slug": f"{unique_slug}-email",
        "owner_email": "not-an-email",
        "password": "securepassword"
    }
    
    res_email = client.post("/api/auth/register", json=invalid_email_payload)
    assert res_email.status_code == 422

    # 3. Teste Slug com caracteres proibidos
    # O frontend previne, mas o backend deve bloquear também (regex ^[a-z0-9-]+$)
    bad_slug_payload = {
        "company_name": "Test Bad Slug",
        "company_slug": "Slug Com Espaço e Maiuscula",
        "owner_email": "slug@test.com",
        "password": "securepassword"
    }
    
    res_slug = client.post("/api/auth/register", json=bad_slug_payload)
    assert res_slug.status_code == 422