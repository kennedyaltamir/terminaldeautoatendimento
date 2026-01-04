from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_delivery_pod_flow():
    """
    Testa o fluxo de Proof of Delivery (POD):
    1. Cria pedido de Delivery (Deve gerar código).
    2. Despacha pedido.
    3. Tenta finalizar sem código (Deve falhar).
    4. Tenta finalizar com código errado (Deve falhar).
    5. Finaliza com código certo (Deve passar).
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(name=f"POD Corp {unique_id}", slug=f"pod-{unique_id}", owner_email=f"pod-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    driver = Employee(
        company_id=company.id,
        name="Driver POD",
        email=f"driver-{unique_id}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver)
    db.commit()
    
    # Extrair IDs primitivos antes de fechar a sessão
    driver_id = driver.id
    company_slug = company.slug
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Criar Pedido Delivery
    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "delivery",
        "customer_name": "POD Client",
        "customer_phone": "11999999999",
        "delivery_address": "Rua POD",
        "items": [] 
    }
    
    # Precisamos de um produto para o pedido ser válido
    from app.models import Category, Product
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Item", price=10)
    db.add(prod)
    db.commit()
    
    payload["items"] = [{"product_id": prod.id, "quantity": 1}]
    
    # Usa a variável primitiva company_slug
    res_create = client.post(f"/api/{company_slug}/orders", json=payload)
    assert res_create.status_code == 201
    order_id = res_create.json()["id"]
    
    # Verificar se gerou código
    # Não precisamos de refresh aqui se usarmos query direta
    order = db.query(Order).filter(Order.id == order_id).first()
    assert order.delivery_code is not None
    assert len(order.delivery_code) == 4
    correct_code = order.delivery_code
    
    # Mover para READY (Simulando cozinha)
    order.status = OrderStatus.READY
    db.commit()
    
    # Fecha a sessão APÓS extrair tudo que precisamos
    db.close()

    # 3. Despachar (Usa driver_id primitivo)
    res_dispatch = client.patch(f"/api/admin/delivery/orders/{order_id}/dispatch", headers=headers, json={"driver_id": driver_id})
    assert res_dispatch.status_code == 200

    # 4. Tentar finalizar SEM código
    res_fail_1 = client.patch(f"/api/admin/delivery/orders/{order_id}/complete", headers=headers, json={})
    assert res_fail_1.status_code == 400
    assert "obrigatório" in res_fail_1.json()["detail"]

    # 5. Tentar finalizar com código ERRADO
    res_fail_2 = client.patch(f"/api/admin/delivery/orders/{order_id}/complete", headers=headers, json={"code": "0000"})
    assert res_fail_2.status_code == 403
    assert "incorreto" in res_fail_2.json()["detail"]

    # 6. Finalizar com código CERTO
    res_success = client.patch(f"/api/admin/delivery/orders/{order_id}/complete", headers=headers, json={"code": correct_code})
    assert res_success.status_code == 200
    assert res_success.json()["message"] == "Entrega finalizada"