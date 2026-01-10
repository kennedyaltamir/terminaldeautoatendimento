# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 10:20:00
import pytest
from app.models import Order, OrderStatus, OrderType, Company, PaymentStatus
from app.core.security import create_access_token
from datetime import datetime
from decimal import Decimal
import uuid

def test_delivery_lifecycle(client, db_session):
    """
    Testa o fluxo de vida de uma entrega usando fixtures de banco de teste.
    """
    # 1. Setup Empresa e Usuário
    unique_id = uuid.uuid4().hex[:6]
    email = f"admin-{unique_id}@mesaflow.com"
    company = Company(
        name="Delivery Test Corp",
        slug=f"del-{unique_id}",
        owner_email=email,
        password_hash="hash"
    )
    db_session.add(company)
    db_session.commit()

    # 2. Criar Pedido READY
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        payment_status=PaymentStatus.PAID,
        customer_name="Delivery Tester",
        delivery_address="Rua Teste, 123",
        delivery_code="1234",
        total_amount=Decimal("50.00"),
        created_at=datetime.now()
    )
    db_session.add(order)
    db_session.commit()
    order_id = str(order.id)

    # 3. Token de Acesso (Com company_id para RLS)
    token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company", "company_id": str(company.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Listar Pedidos de Delivery
    list_res = client.get("/api/admin/delivery/orders", headers=headers)
    assert list_res.status_code == 200

    # 5. Despacho
    dispatch_res = client.patch(f"/api/admin/delivery/orders/{order_id}/dispatch", headers=headers, json={})
    assert dispatch_res.status_code == 200

    # 6. Finalização (POD)
    complete_res = client.patch(f"/api/admin/delivery/orders/{order_id}/complete", headers=headers, json={"code": "1234"})
    assert complete_res.status_code == 200
