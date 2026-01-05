from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_dispatch_order_with_driver():
    """
    Testa o fluxo de despacho de um pedido atribuindo um entregador.
    1. Cria Empresa e Entregador.
    2. Cria Pedido (READY).
    3. Despacha o pedido atribuindo o entregador.
    4. Verifica se o pedido foi atualizado corretamente.
    """
    # 1. Setup
    unique_slug = f"dispatch-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Dispatch Corp",
        slug=unique_slug,
        owner_email=f"dispatch-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Criar Entregador
    driver = Employee(
        company_id=company.id,
        name="Motoboy Teste",
        email=f"driver-{uuid.uuid4().hex[:6]}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver)
    db.commit()
    
    # Criar Pedido Pronto
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        customer_name="Cliente Delivery",
        total_amount=50.00
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    driver_id = driver.id
    
    # Token Admin
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Despachar Pedido
    payload = {"driver_id": driver_id}
    res = client.patch(f"/api/admin/delivery/orders/{order_id}/dispatch", headers=headers, json=payload)
    
    assert res.status_code == 200
    assert res.json()["message"] == "Pedido despachado"

    # 3. Verificar Estado do Pedido
    # Reabrir sessão para verificar
    db = SessionLocal()
    updated_order = db.query(Order).filter(Order.id == order_id).first()
    
    assert updated_order.status == OrderStatus.DELIVERING
    assert updated_order.driver_id == driver_id
    
    db.close()