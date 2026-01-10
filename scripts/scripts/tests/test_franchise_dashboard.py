from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from app.core.security import create_access_token
from decimal import Decimal
from datetime import datetime
import uuid

client = TestClient(app)

def test_franchise_aggregation():
    """
    Testa se o dashboard consolida dados de múltiplas lojas do mesmo dono.
    Cenário:
    1. Cria Loja A e Loja B (mesmo owner_email).
    2. Cria pedidos em ambas.
    3. Verifica se o endpoint retorna a soma correta e o detalhamento.
    """
    
    # 1. Setup
    owner_email = f"franchise-{uuid.uuid4().hex[:6]}@test.com"
    db = SessionLocal()
    
    # Loja A
    company_a = Company(name="Loja A", slug=f"loja-a-{uuid.uuid4().hex[:4]}", owner_email=owner_email)
    db.add(company_a)
    
    # Loja B
    company_b = Company(name="Loja B", slug=f"loja-b-{uuid.uuid4().hex[:4]}", owner_email=owner_email)
    db.add(company_b)
    
    db.commit()
    
    id_a = company_a.id
    id_b = company_b.id
    
    # 2. Pedidos
    # Loja A: 2 pedidos de R$ 50 = R$ 100
    for _ in range(2):
        db.add(Order(
            company_id=id_a, total_amount=50.00, 
            status=OrderStatus.DELIVERED, payment_status=PaymentStatus.PAID,
            created_at=datetime.now()
        ))
        
    # Loja B: 1 pedido de R$ 200 = R$ 200
    db.add(Order(
        company_id=id_b, total_amount=200.00, 
        status=OrderStatus.DELIVERED, payment_status=PaymentStatus.PAID,
        created_at=datetime.now()
    ))
    
    db.commit()
    
    # Token (Logado como dono)
    token = create_access_token(data={"sub": owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 3. Request
    res = client.get("/api/admin/franchise/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # 4. Validação Global
    # Total esperado: 100 + 200 = 300
    assert float(data["total_revenue"]) == 300.00
    assert data["total_orders"] == 3
    
    # 5. Validação Individual
    stores = data["stores"]
    assert len(stores) == 2
    
    # Loja B deve estar em primeiro (Ranking por receita)
    assert stores[0]["name"] == "Loja B"
    assert float(stores[0]["revenue"]) == 200.00
    
    assert stores[1]["name"] == "Loja A"
    assert float(stores[1]["revenue"]) == 100.00