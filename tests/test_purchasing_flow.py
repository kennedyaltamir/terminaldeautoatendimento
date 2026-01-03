from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Ingredient, Supplier
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_purchase_order_generation():
    """
    Testa o fluxo de geração de ordem de compra:
    1. Cria Fornecedor e Ingrediente com estoque baixo.
    2. Consulta a prévia de compras (Preview).
    3. Gera o HTML de impressão.
    """
    # 1. Setup
    unique_slug = f"purchase-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Purchase Corp",
        slug=unique_slug,
        owner_email=f"buyer-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    supplier = Supplier(company_id=company.id, name="Fornecedor A")
    db.add(supplier)
    db.commit()
    
    # Ingrediente com estoque 5 (Mínimo 10) -> Deve comprar
    ing = Ingredient(
        company_id=company.id,
        name="Item em Falta",
        unit="un",
        current_stock=Decimal("5.00"),
        min_stock_alert=Decimal("10.00"),
        cost_per_unit=Decimal("2.00"),
        supplier_id=supplier.id
    )
    db.add(ing)
    db.commit()
    
    supplier_id = supplier.id
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Preview
    res_preview = client.get("/api/admin/inventory/purchase-orders/preview", headers=headers)
    assert res_preview.status_code == 200
    data = res_preview.json()
    
    assert len(data) > 0
    order = data[0]
    assert order["supplier_name"] == "Fornecedor A"
    # Meta: Dobro do mínimo (20) - Atual (5) = 15
    assert float(order["items"][0]["to_buy"]) == 15.0
    # Custo: 15 * 2.00 = 30.00
    assert float(order["total_estimated"]) == 30.00

    # 3. Print HTML
    res_print = client.get(f"/api/admin/inventory/purchase-orders/{supplier_id}/print", headers=headers)
    assert res_print.status_code == 200
    assert "text/html" in res_print.headers["content-type"]
    assert "Ordem de Compra" in res_print.text
    assert "Fornecedor A" in res_print.text
    assert "Item em Falta" in res_print.text