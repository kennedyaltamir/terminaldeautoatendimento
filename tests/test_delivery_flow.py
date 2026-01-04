from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, OrderType, Company, PaymentStatus
from datetime import datetime
import pytest

client = TestClient(app)

def test_delivery_lifecycle():
    """
    Testa o ciclo de vida de uma entrega:
    1. Login como Admin.
    2. Criação de pedido READY.
    3. Listagem.
    4. Despacho e Finalização.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        payment_status=PaymentStatus.PAID,
        customer_name="Delivery Tester",
        delivery_address="Rua Teste, 123",
        total_amount=50.00,
        created_at=datetime.now()
    )
    db.add(order)
    db.commit()
    order_id = str(order.id)
    db.close()

    # 3. Listar
    list_res = client.get("/api/admin/delivery/orders", headers=headers)
    assert list_res.status_code == 200
    
    # 4. Fluxo de Status
    # Enviar json={} para satisfazer o Pydantic (DispatchOrderRequest)
    dispatch_res = client.patch(f"/api/admin/delivery/orders/{order_id}/dispatch", headers=headers, json={})
    assert dispatch_res.status_code == 200
    
    # CORREÇÃO: Enviar json={} para satisfazer o Pydantic (CompleteDeliveryRequest)
    complete_res = client.patch(f"/api/admin/delivery/orders/{order_id}/complete", headers=headers, json={})
    assert complete_res.status_code == 200