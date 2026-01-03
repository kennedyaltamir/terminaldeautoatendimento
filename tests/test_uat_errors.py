from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category, Order, OrderStatus
from decimal import Decimal
import uuid

client = TestClient(app)

def test_err_02_stock_race_condition():
    """
    ERR-02: Estoque Negativo (Simulação Lógica)
    Tenta vender 2 unidades quando só existe 1.
    """
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(name=f"Err {unique_id}", slug=f"err-{unique_id}", owner_email=f"err-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    
    # Produto com estoque 1
    prod = Product(
        category_id=cat.id, 
        name="Last Item", 
        price=10, 
        track_stock=True, 
        stock_quantity=1
    )
    db.add(prod)
    db.commit()
    
    # Extrair dados antes de fechar
    prod_id = prod.id
    slug = company.slug
    db.close()
    
    # Pedido 1 (Sucesso)
    payload = {
        "table_id": None, "qr_token": "staff-override",
        "order_type": "takeout", # <--- CORREÇÃO: Tipo Takeout
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    res1 = client.post(f"/api/{slug}/orders", json=payload)
    assert res1.status_code == 201
    
    # Pedido 2 (Falha - Estoque Insuficiente)
    res2 = client.post(f"/api/{slug}/orders", json=payload)
    assert res2.status_code == 400
    assert "Estoque insuficiente" in res2.json()["detail"]

def test_err_03_payment_failure():
    """
    ERR-03: Falha no Pagamento Online
    O pedido deve ser criado, mas o pagamento falha.
    """
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    company = Company(name=f"Pay {unique_id}", slug=f"pay-{unique_id}", owner_email=f"pay-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    prod = Product(category_id=cat.id, name="Item", price=10)
    db.add(prod)
    db.commit()
    
    # Extrair dados antes de fechar
    prod_id = prod.id
    slug = company.slug
    db.close()
    
    # 1. Criar Pedido
    payload = {
        "table_id": None, "qr_token": "staff-override",
        "order_type": "takeout", # <--- CORREÇÃO: Tipo Takeout
        "payment_method": "online",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    res_order = client.post(f"/api/{slug}/orders", json=payload)
    assert res_order.status_code == 201
    order_id = res_order.json()["id"]
    
    # 2. Simular Falha no Pagamento (Cartão final 0000 no mock)
    pay_payload = {
        "order_id": order_id,
        "card_number": "4111111111110000", # Gatilho de erro no mock
        "card_holder": "Fail Test",
        "expiration": "12/30",
        "cvv": "123"
    }
    
    res_pay = client.post("/api/payments/process", json=pay_payload)
    assert res_pay.status_code == 400
    assert "recusado" in res_pay.json()["detail"]
    
    # 3. Verificar se o pedido continua com pagamento falho
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    
    # Pedidos de staff nascem ACCEPTED, mas o pagamento deve ser FAILED
    assert order.status in [OrderStatus.ACCEPTED, OrderStatus.PENDING]
    assert order.payment_status == "failed"
    db.close()