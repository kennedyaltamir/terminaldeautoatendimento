from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def setup_logistics_env():
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    # Empresa
    company = Company(
        name=f"Logistics {unique_id}",
        slug=f"log-{unique_id}",
        owner_email=f"log-{unique_id}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Motorista João
    driver_joao = Employee(
        company_id=company.id,
        name="João Motoboy",
        email=f"joao-{unique_id}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver_joao)
    
    # Motorista Maria
    driver_maria = Employee(
        company_id=company.id,
        name="Maria Motogirl",
        email=f"maria-{unique_id}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver_maria)
    db.commit()
    
    # Tokens
    token_admin = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    token_joao = create_access_token(data={"sub": driver_joao.email, "role": "driver", "account_type": "employee", "company_id": str(company.id)})
    
    return db, company, driver_joao, driver_maria, token_admin, token_joao

def test_log_01_dispatch_pool():
    """LOG-01: Despacho sem motorista vai para o pool geral"""
    db, company, _, _, token_admin, token_driver = setup_logistics_env()
    
    # Pedido Pronto
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        total_amount=50.00
    )
    db.add(order)
    db.commit()
    order_id = str(order.id)
    db.close()
    
    # Admin despacha sem driver_id
    headers = {"Authorization": f"Bearer {token_admin}"}
    res = client.patch(f"/api/admin/delivery/orders/{order_id}/dispatch", headers=headers, json={})
    assert res.status_code == 200
    
    # Motorista vê o pedido?
    headers_driver = {"Authorization": f"Bearer {token_driver}"}
    res_list = client.get("/api/admin/delivery/orders", headers=headers_driver)
    orders = res_list.json()
    
    target = next((o for o in orders if o["id"] == order_id), None)
    assert target is not None
    assert target["status"] == "delivering"
    assert target["driver_id"] is None # Está no pool

def test_log_02_specific_assignment():
    """LOG-02: Atribuição específica para o João"""
    db, company, driver_joao, _, token_admin, _ = setup_logistics_env()
    
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.READY,
        total_amount=50.00
    )
    db.add(order)
    db.commit()
    
    # Extrair dados antes de fechar a sessão
    order_id = str(order.id)
    joao_id = driver_joao.id
    
    db.close()
    
    # Admin despacha para João
    headers = {"Authorization": f"Bearer {token_admin}"}
    res = client.patch(
        f"/api/admin/delivery/orders/{order_id}/dispatch", 
        headers=headers, 
        json={"driver_id": joao_id}
    )
    assert res.status_code == 200
    
    # Verificar no banco
    db = SessionLocal()
    updated = db.query(Order).filter(Order.id == order_id).first()
    assert updated.driver_id == joao_id
    db.close()