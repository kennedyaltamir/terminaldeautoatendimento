from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_credential_masking():
    """
    Testa se o token do Mercado Pago é mascarado na leitura e preservado na escrita.
    """
    # 1. Setup
    unique_slug = f"sec-{uuid.uuid4().hex[:6]}"
    real_token = "APP_USR-1234567890-REAL-TOKEN"
    
    db = SessionLocal()
    company = Company(
        name="Security Corp",
        slug=unique_slug,
        owner_email=f"sec-{uuid.uuid4().hex[:6]}@test.com",
        mp_access_token=real_token
    )
    db.add(company)
    db.commit()
    company_id = company.id
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Teste de Leitura (GET)
    res_get = client.get("/api/admin/company/me", headers=headers)
    assert res_get.status_code == 200
    data = res_get.json()
    
    # O token deve vir mascarado
    assert data["mp_access_token"] != real_token
    assert "****" in data["mp_access_token"]
    assert data["mp_access_token"].startswith("APP_USR-")

    # 3. Teste de Escrita com Máscara (PATCH)
    # O frontend envia de volta o valor mascarado ao salvar outros campos
    payload = {
        "name": "Security Corp Updated",
        "mp_access_token": data["mp_access_token"] # Envia o mascarado
    }
    
    res_patch = client.patch("/api/admin/company/me", headers=headers, json=payload)
    assert res_patch.status_code == 200
    
    # 4. Verificar Integridade no Banco
    # O token real NÃO deve ter sido alterado para "****"
    db = SessionLocal()
    updated_company = db.query(Company).filter(Company.id == company_id).first()
    assert updated_company.mp_access_token == real_token
    assert updated_company.name == "Security Corp Updated"
    db.close()

    print("✅ Teste de segurança de credenciais passou!")