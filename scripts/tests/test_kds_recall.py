from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company
from app.core.security import create_access_token
from datetime import datetime
import uuid

client = TestClient(app)

def test_kds_recall_flow():
    """
    Testa o fluxo de Recall.
    """
    # 1. Setup Isolado
    unique_slug = f"recall-{uuid.uuid4().hex[:6]}"
    email = f"recall-{unique_slug}@test.com"
    
    db = SessionLocal()
    company = Company(name="Recall Corp", slug=unique_slug, owner_email=email)
    db.add(company)
    db.commit()

    # 2. Criar pedido finalizado
    order = Order(
        company_id=company.id,
        table_id=1,
        total_amount=50.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now(),
        finished_at=datetime.now() # Essencial para o filtro
    )
    db.add(order)
    db.commit()
    order_id = str(order.id)
    
    token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 3. Buscar na lista de Recall
    recall_res = client.get(f"/api/admin/{unique_slug}/orders/recent-completed", headers=headers)
    assert recall_res.status_code == 200
    recent_orders = recall_res.json()
    
    assert any(o["id"] == order_id for o in recent_orders)
