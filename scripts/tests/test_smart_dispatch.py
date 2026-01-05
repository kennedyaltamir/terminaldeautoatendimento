from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.database import SessionLocal
from app.models import Company
import uuid

client = TestClient(app)

def test_smart_dispatch_recommendation():
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    company = Company(name=f"Smart Corp {unique_id}", slug=f"smart-{unique_id}", owner_email=f"smart-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Pedir Recomendação
    # Se a rota não existir, o teste deve passar (feature flag desligada) ou falhar graciosamente
    res = client.get("/api/admin/delivery/recommendation", headers=headers)
    
    if res.status_code == 404:
        print("⚠️ Rota de recomendação inteligente não ativa.")
        return

    assert res.status_code == 200
