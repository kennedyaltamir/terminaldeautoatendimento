from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, CompanySegment
import uuid

client = TestClient(app)

def test_registration_with_segment_and_strong_password():
    """
    Testa o novo fluxo de registro com:
    1. Segmento (Verticalização)
    2. Validação de Senha Forte
    3. Criação de Trial
    """
    
    unique_slug = f"test-saas-{uuid.uuid4().hex[:6]}"
    unique_email = f"saas-{uuid.uuid4().hex[:6]}@test.com"
    
    # 1. Tentar senha fraca (Deve falhar)
    weak_payload = {
        "company_name": "Weak Pass Corp",
        "company_slug": f"{unique_slug}-weak",
        "owner_email": unique_email,
        "password": "weak", # Curta
        "segment": "hotel"
    }
    res_weak = client.post("/api/auth/register", json=weak_payload)
    assert res_weak.status_code == 422
    
    # 2. Tentar senha sem número (Deve falhar)
    alpha_payload = weak_payload.copy()
    alpha_payload["password"] = "passwordonly"
    res_alpha = client.post("/api/auth/register", json=alpha_payload)
    assert res_alpha.status_code == 422

    # 3. Registro Correto (Senha Forte + Segmento)
    strong_payload = {
        "company_name": "Hotel Plaza Test",
        "company_slug": unique_slug,
        "owner_email": unique_email,
        "password": "StrongPass123",
        "segment": "hotel",
        "owner_role": "Gerente Geral",
        "owner_phone": "11999999999"
    }
    
    res_success = client.post("/api/auth/register", json=strong_payload)
    assert res_success.status_code == 201
    
    # 4. Verificar Banco de Dados
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == unique_slug).first()
    
    assert company is not None
    assert company.segment == CompanySegment.HOTEL
    assert company.owner_role == "Gerente Geral"
    assert company.trial_ends_at is not None # Trial deve ter sido criado
    
    db.close()