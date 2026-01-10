from app.models import OrderStatus, PaymentStatus, Company, Product, Category
from decimal import Decimal
import uuid

def test_online_payment_flow(client, db_session):
    # 1. Setup
    unique_slug = f"pay-online-{uuid.uuid4().hex[:6]}"
    company = Company(name="Pay Online Corp", slug=unique_slug, owner_email=f"pay-{unique_slug}@test.com")
    db_session.add(company)
    db_session.commit()

    cat = Category(company_id=company.id, name="Geral")
    db_session.add(cat)
    db_session.commit()
    
    prod = Product(category_id=cat.id, name="Item", price=Decimal("10.00"))
    db_session.add(prod)
    db_session.commit()

    # 2. Criar Pedido
    order_payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Online Payer",
        "payment_method": "online",
        "items": [{"product_id": prod.id, "quantity": 1}]
    }
    order_res = client.post(f"/api/{unique_slug}/orders", json=order_payload)
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    # 3. Processar Pagamento Online (Simulado)
    payment_payload = {
        "order_id": order_id,
        "card_number": "4111111111111111",
        "card_holder": "TEST USER",
        "expiration": "12/30",
        "cvv": "123"
    }
    pay_res = client.post("/api/payments/process", json=payment_payload)
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "approved"

def test_online_payment_declined(client, db_session):
    # 1. Setup
    unique_slug = f"pay-dec-{uuid.uuid4().hex[:6]}"
    company = Company(name="Pay Dec Corp", slug=unique_slug, owner_email=f"dec-{unique_slug}@test.com")
    db_session.add(company)
    db_session.commit()

    cat = Category(company_id=company.id, name="Geral")
    db_session.add(cat)
    db_session.commit()
    
    prod = Product(category_id=cat.id, name="Item", price=Decimal("10.00"))
    db_session.add(prod)
    db_session.commit()

    # 2. Criar Pedido
    order_payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Bad Payer",
        "payment_method": "online",
        "items": [{"product_id": prod.id, "quantity": 1}]
    }
    order_res = client.post(f"/api/{unique_slug}/orders", json=order_payload)
    assert order_res.status_code == 201
    order_id = order_res.json()["id"]

    # 3. Tentar pagar com cartão final 0000 (Regra de recusa simulada)
    payment_payload = {
        "order_id": order_id,
        "card_number": "4111111111110000",
        "card_holder": "BAD USER",
        "expiration": "12/30",
        "cvv": "123"
    }
    pay_res = client.post("/api/payments/process", json=payment_payload)
    assert pay_res.status_code == 400
    assert "recusado" in pay_res.json()["detail"]
