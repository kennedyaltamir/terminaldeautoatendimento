from app.models import Ingredient, Product, Company, TableSession, Table, ProductRecipe
from decimal import Decimal
import uuid

def test_recipe_deduction(client, db_session):
    """
    Testa se ao vender um produto, os ingredientes da ficha técnica são baixados.
    """
    # 1. Setup do Banco de Dados
    unique_slug = f"recipe-{uuid.uuid4().hex[:6]}"
    company = Company(name="Recipe Corp", slug=unique_slug, owner_email=f"recipe-{unique_slug}@test.com")
    db_session.add(company)
    db_session.commit()

    # Ingrediente: Carne (10kg)
    carne = Ingredient(
        company_id=company.id,
        name="Carne Moída",
        unit="kg",
        current_stock=Decimal("10.000"),
        cost_per_unit=Decimal("20.00")
    )
    db_session.add(carne)
    db_session.commit()

    # Produto: X-Bacon
    from app.models import Category
    cat = Category(company_id=company.id, name="Lanches")
    db_session.add(cat)
    db_session.commit()
    
    xbacon = Product(category_id=cat.id, name="X-Bacon", price=Decimal("20.00"), track_stock=False)
    db_session.add(xbacon)
    db_session.commit()

    # Receita: 0.180kg por unidade
    recipe = ProductRecipe(product_id=xbacon.id, ingredient_id=carne.id, quantity_required=Decimal("0.180"))
    db_session.add(recipe)
    db_session.commit()

    # Mesa e Sessão
    table = Table(company_id=company.id, table_number=1, qr_token="token")
    db_session.add(table)
    db_session.commit()

    session = TableSession(
        company_id=company.id,
        table_id=table.id,
        customer_name="Stock Tester",
        session_token=str(uuid.uuid4()),
        access_pin="1234",
        is_active=True
    )
    db_session.add(session)
    db_session.commit()

    # 3. Vender 2 X-Bacon
    order_payload = {
        "table_id": table.id,
        "qr_token": table.qr_token,
        "customer_name": "Stock Tester",
        "items": [{"product_id": xbacon.id, "quantity": 2}]
    }

    res_order = client.post(f"/api/{unique_slug}/orders", json=order_payload)
    assert res_order.status_code == 201

    # 4. Verificar estoque final
    db_session.refresh(carne)
    expected_stock = 10.000 - (0.180 * 2)
    
    # Usar float para comparação simples
    assert float(carne.current_stock) == expected_stock
