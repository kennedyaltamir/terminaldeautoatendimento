from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from app.core.security import create_access_token
from decimal import Decimal
from datetime import datetime
import uuid

client = TestClient(app)

def test_marketing_and_franchise_contracts():
    """
    Valida se os endpoints de Marketing e Franquia retornam os dados
    no formato esperado pelo Frontend (React).
    """
    # 1. Setup
    owner_email = f"ent-contract-{uuid.uuid4().hex[:6]}@test.com"
    db = SessionLocal()
    
    company = Company(
        name="Enterprise Corp", 
        slug=f"ent-{uuid.uuid4().hex[:4]}", 
        owner_email=owner_email,
        loyalty_percentage=Decimal("5.00")
    )
    db.add(company)
    db.commit()
    
    token = create_access_token(data={"sub": owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Teste Marketing (IA Trigger)
    res_mkt = client.post("/api/admin/marketing/recommendations/generate", headers=headers)
    assert res_mkt.status_code == 202
    assert "status" in res_mkt.json()
    
    # 3. Teste Franquia (Dashboard)
    res_fran = client.get("/api/admin/franchise/dashboard", headers=headers)
    assert res_fran.status_code == 200
    data = res_fran.json()
    
    # Validação de Tipagem (TypeScript Interface)
    assert isinstance(data["total_revenue"], (int, float))
    assert isinstance(data["total_orders"], int)
    assert isinstance(data["stores"], list)
    
    print("✅ Contratos de Frontend Enterprise validados!")
