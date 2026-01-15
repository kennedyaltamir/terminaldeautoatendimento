from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_marketing_ai_trigger():
    """
    Testa se o endpoint de geração de recomendações (IA) está acessível e responde corretamente.
    """
    # 1. Setup
    unique_slug = f"mkt-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Marketing Corp",
        slug=unique_slug,
        owner_email=f"mkt-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Trigger IA
    res = client.post("/api/admin/marketing/recommendations/generate", headers=headers)
    
    # O endpoint retorna 202 Accepted pois roda em background
    assert res.status_code == 202
    assert "iniciado" in res.json()["message"]
    assert res.json()["status"] == "processing"
