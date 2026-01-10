from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_system_integrity_for_handover():
    unique_slug = f"handover-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    
    company = Company(
        name="Handover Corp",
        slug=unique_slug,
        owner_email=f"admin-{unique_slug}@test.com",
        marketplace_fee_percentage=Decimal("2.00")
    )
    db.add(company)
    db.commit()
    
    driver = Employee(
        company_id=company.id,
        name="Driver Test",
        email=f"driver-{unique_slug}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver)
    db.commit()
    
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        customer_name="Handover Client",
        total_amount=Decimal("100.00")
    )
    db.add(order)
    db.commit()
    
    company_id = company.id
    driver_id = driver.id
    order_id = str(order.id)
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    res_dispatch = client.patch(
        f"/api/admin/delivery/orders/{order_id}/dispatch", 
        headers=headers, 
        json={"driver_id": driver_id}
    )
    
    assert res_dispatch.status_code == 200
    assert res_dispatch.json()["message"] == "Pedido despachado"

    db = SessionLocal()
    updated_order = db.query(Order).filter(Order.id == order_id).first()
    assert updated_order.status == OrderStatus.DELIVERING
    assert updated_order.driver_id == driver_id
    db.close()