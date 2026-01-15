from fastapi.testclient import TestClient
from app.main import app
from app.models import PaymentStatus, Company, Category, Product
from app.database import SessionLocal
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_payment_confirmation_flow():
    """Valida se o admin consegue confirmar o pagamento de um pedido"""
    # 1. Setup
    unique_slug = f"pay-flow-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(name="Pay Flow Corp", slug=unique_slug, owner_email=f"pf-{unique_slug}@test.com")
    db.add(company)
    db.commit()

    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    prod = Product(category_id=cat.id, name="Item", price=Decimal("10.00"))
    db.add(prod)
    db.commit()
    
    # Extrair ID primitivo para evitar DetachedInstanceError
    prod_id = prod.id

    # Token Admin
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Criar um pedido via API
    order_payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Teste Pagamento",
        "payment_method": "pix",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    order_res = client.post(f"/api/{unique_slug}/orders", json=order_payload)
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    # 3. Confirmar Pagamento
    pay_res = client.patch(f"/api/admin/orders/{order_id}/payment", headers=headers, json={"payment_status": "paid"})
    assert pay_res.status_code == 200

    # 4. Verificar se as métricas agora contam este pedido
    metrics_res = client.get("/api/admin/metrics", headers=headers)
    assert metrics_res.status_code == 200
    assert metrics_res.json()["total_orders"] >= 1
