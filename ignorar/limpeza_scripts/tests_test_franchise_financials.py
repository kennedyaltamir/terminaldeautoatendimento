import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderItem, Product, Category, ProductRecipe, Ingredient, OrderStatus, PaymentStatus
from app.core.security import create_access_token
from decimal import Decimal
from datetime import datetime
import uuid

client = TestClient(app)

def test_franchise_profitability_logic():
    """
    Valida o cálculo de CMV e Lucro no Dashboard de Franquia.
    Cenário:
    - Produto: R$ 20.00
    - Ingrediente: R$ 5.00 (Custo)
    - Venda: 10 unidades
    - Esperado: Receita 200, CMV 50, Lucro 150
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    email = f"franchise-fin-{unique_id}@test.com"
    db = SessionLocal()

    company = Company(name="Loja Financeira", slug=f"fin-{unique_id}", owner_email=email)
    db.add(company)
    db.commit()

    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()

    ing = Ingredient(company_id=company.id, name="Insumo", cost_per_unit=Decimal("5.00"), current_stock=100)
    db.add(ing)
    db.commit()

    prod = Product(category_id=cat.id, name="Produto", price=Decimal("20.00"))
    db.add(prod)
    db.commit()

    recipe = ProductRecipe(product_id=prod.id, ingredient_id=ing.id, quantity_required=Decimal("1.00"))
    db.add(recipe)
    db.commit()

    # 2. Criar 10 Pedidos Pagos
    # IMPORTANTE: Forçamos o created_at para o momento atual para bater com o filtro "Hoje" da API
    now = datetime.now()

    for _ in range(10):
        order = Order(
            company_id=company.id, 
            total_amount=Decimal("20.00"), 
            status=OrderStatus.DELIVERED, 
            payment_status=PaymentStatus.PAID,
            created_at=now # Injeção manual para evitar erro de timezone do servidor
        )
        db.add(order)
        db.commit()
        
        item = OrderItem(order_id=order.id, product_id=prod.id, quantity=1, unit_price=Decimal("20.00"))
        db.add(item)
        db.commit()

    token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 3. Request Dashboard
    res = client.get("/api/admin/franchise/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()

    # 4. Validações
    assert len(data["stores"]) > 0
    store = data["stores"][0]
    
    # Receita: 10 * 20 = 200
    assert store["revenue"] == 200.0
    # CMV: 10 * 5 = 50
    assert store["cmv"] == 50.0
    # Lucro: 200 - 50 = 150
    assert store["profit"] == 150.0
    # Margem: (150 / 200) * 100 = 75%
    assert store["margin_percent"] == 75.0

    print(f"\n✅ Lucratividade validada: Receita R$ {store['revenue']} | Lucro R$ {store['profit']}")

if __name__ == "__main__":
    test_franchise_profitability_logic()
