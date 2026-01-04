from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Ingredient, ProductRecipe, Order, OrderStatus, PaymentStatus
from decimal import Decimal
import uuid
import pytest

client = TestClient(app)

def test_synchronous_stock_deduction():
    """
    Testa se a baixa de estoque ocorre de forma síncrona e impede a venda se não houver estoque.
    """
    # 1. Setup
    unique_slug = f"sync-stock-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Sync Stock Corp",
        slug=unique_slug,
        owner_email=f"stock-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Ingrediente com estoque 1.0 (Este será o gargalo do teste)
    ing = Ingredient(
        company_id=company.id,
        name="Ingrediente Crítico",
        unit="un",
        current_stock=Decimal("1.00"),
        min_stock_alert=Decimal("0.00"),
        cost_per_unit=Decimal("10.00")
    )
    db.add(ing)
    db.commit()
    
    # Produto que usa 1.0 do ingrediente
    from app.models import Category
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    
    prod = Product(
        category_id=cat.id,
        name="Produto Crítico",
        price=Decimal("20.00"),
        is_available=True,
        track_stock=True,
        stock_quantity=10 # Estoque suficiente no produto para não bloquear antes do ingrediente
    )
    db.add(prod)
    db.commit()
    
    recipe = ProductRecipe(
        product_id=prod.id,
        ingredient_id=ing.id,
        quantity_required=Decimal("1.00")
    )
    db.add(recipe)
    db.commit()
    
    # Capturar IDs primitivos antes de fechar a sessão para evitar DetachedInstanceError
    prod_id = prod.id
    ing_id = ing.id
    company_id = company.id 
    
    db.close()

    # 2. Pedido 1 (Sucesso - Consome 1.0 do Ingrediente)
    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "items": [{"product_id": prod_id, "quantity": 1}]
    }
    
    res1 = client.post(f"/api/{unique_slug}/orders", json=payload)
    assert res1.status_code == 201
    
    # 3. Pedido 2 (Falha - Ingrediente Esgotado)
    # O ingrediente foi de 1.0 para 0.0 no pedido anterior.
    res2 = client.post(f"/api/{unique_slug}/orders", json=payload)
    assert res2.status_code == 400
    
    # O erro pode ser "Produto indisponível" (se a Regra 86 rodou rápido) ou "Ingrediente esgotado"
    error_msg = res2.json()["detail"].lower()
    assert "esgotado" in error_msg or "indisponível" in error_msg or "insuficiente" in error_msg
    
    # 4. Verificar se o pedido 2 NÃO foi criado
    db = SessionLocal()
    # Usa company_id (int) em vez de company.id (objeto detached)
    orders_count = db.query(Order).filter(Order.company_id == company_id).count()
    assert orders_count == 1
    
    # Verificar estoque final do ingrediente (Deve ser 0)
    final_ing = db.query(Ingredient).filter(Ingredient.id == ing_id).first()
    assert final_ing.current_stock == 0
    
    db.close()