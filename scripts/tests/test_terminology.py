from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, CompanySegment
import uuid

client = TestClient(app)

def test_segment_persistence():
    """
    Testa se o segmento é salvo corretamente no banco e retornado na API.
    Isso é a base para o frontend decidir qual dicionário usar.
    """
    # 1. Setup
    unique_slug = f"hotel-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    
    company = Company(
        name="Hotel Teste",
        slug=unique_slug,
        owner_email=f"hotel-{uuid.uuid4().hex[:6]}@test.com",
        segment=CompanySegment.HOTEL
    )
    db.add(company)
    db.commit()
    
    # Token
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Verificar API
    res = client.get("/api/admin/company/me", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    assert data["segment"] == "hotel"
    
    # 3. Verificar se o frontend receberia o dado correto para mudar "Mesa" para "Quarto"
    # (O teste de frontend real seria via Cypress/Playwright, aqui validamos o contrato de dados)