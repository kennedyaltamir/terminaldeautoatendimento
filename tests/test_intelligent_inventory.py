from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Ingredient, ProductRecipe, Table, TableSession
from decimal import Decimal
import uuid
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_automatic_86_rule_and_notification():
    """
    Testa se o ingrediente zerado desativa o produto e chama o WhatsApp.
    """
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    
    # Garantir que a empresa tem um número de WhatsApp para o teste
    company.whatsapp_number = "5511999999999"
    db.commit()
    
    # 1. Criar Ingrediente com estoque baixo (1 unidade)
    pao = Ingredient(
        company_id=company.id,
        name="Pão de Teste Inteligente",
        unit="un",
        current_stock=Decimal("1.000"),
        cost_per_unit=Decimal("1.00")
    )
    db.add(pao)
    db.commit()
    
    # 2. Criar Produto vinculado
    burger = Product(
        category_id=company.categories[0].id,
        name="Burger Inteligente",
        price=Decimal("10.00"),
        is_available=True
    )
    db.add(burger)
    db.commit()
    
    db.add(ProductRecipe(product_id=burger.id, ingredient_id=pao.id, quantity_required=Decimal("1.000")))
    db.commit()

    # 3. Setup de Sessão
    table = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    session = TableSession(
        company_id=company.id, table_id=table.id, customer_name="QA Stock",
        session_token=str(uuid.uuid4()), access_pin="1234", is_active=True
    )
    db.add(session)
    db.commit()
    
    burger_id = burger.id
    db.close()

    # 4. Realizar pedido que zera o estoque
    order_payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "QA Stock",
        "items": [{"product_id": burger_id, "quantity": 1}]
    }

    # Patch no WhatsAppService.notify_low_stock
    with patch("app.services.whatsapp_service.WhatsAppService.notify_low_stock", new_callable=AsyncMock) as mock_ws:
        res = client.post("/api/hamburgueria-ze/orders", json=order_payload)
        assert res.status_code == 201

        # 5. Verificar se o produto foi desativado (Regra 86)
        db = SessionLocal()
        updated_burger = db.query(Product).filter(Product.id == burger_id).first()
        assert updated_burger.is_available is False
        
        # 6. Verificar se o WhatsApp foi chamado (via BackgroundTask)
        mock_ws.assert_called_once()
        db.close()