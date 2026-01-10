from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category
from decimal import Decimal

client = TestClient(app)

def test_order_validation_logic():
    """Garante que o backend processa corretamente pedidos com e sem opções"""
    # 1. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    
    # Garantir horário de funcionamento aberto
    company.opens_at = None
    company.closes_at = None
    db.commit()

    # Pegar produto
    prod = db.query(Product).filter(Product.category.has(company_id=company.id)).first()
    prod_id = prod.id
    prod_price = float(prod.price)
    db.close()

    # 2. Pedido Simples
    payload_simple = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Teste Simples",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    res_simple = client.post("/api/hamburgueria-ze/orders", json=payload_simple)
    assert res_simple.status_code == 201
    assert float(res_simple.json()["total_amount"]) == prod_price
