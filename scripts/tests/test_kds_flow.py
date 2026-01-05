from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_order_status_transition_for_kds():
    # 1. Setup
    unique_slug = f"kds-flow-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(name="KDS Flow Corp", slug=unique_slug, owner_email=f"kds-{unique_slug}@test.com")
    db.add(company)
    db.commit()
    
    order = Order(company_id=company.id, total_amount=10, status=OrderStatus.PENDING)
    db.add(order)
    db.commit()
    order_id = str(order.id)
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Atualizar para PREPARING
    patch_res = client.patch(
        f"/api/admin/orders/{order_id}",
        headers=headers,
        json={"status": "preparing"}
    )
    assert patch_res.status_code == 200
