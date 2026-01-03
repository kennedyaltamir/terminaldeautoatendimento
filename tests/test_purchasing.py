from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Ingredient, Supplier
from decimal import Decimal
import uuid

client = TestClient(app)

def test_shopping_list_generation():
    """
    Testa se o sistema gera a lista de compras corretamente:
    1. Cria Fornecedor.
    2. Cria Ingrediente com estoque BAIXO (abaixo do mínimo).
    3. Cria Ingrediente com estoque ALTO (acima do mínimo).
    4. Verifica se apenas o item baixo aparece na lista.
    """
    
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup de Dados
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Criar Fornecedor
    supplier = Supplier(company_id=company.id, name="Fornecedor Teste")
    db.add(supplier)
    db.commit()
    
    # Ingrediente BAIXO (Deve aparecer)
    # Mínimo 10, Atual 5 -> Deficit 5
    ing_low = Ingredient(
        company_id=company.id,
        name="Item Baixo",
        unit="un",
        current_stock=Decimal("5.000"),
        min_stock_alert=Decimal("10.000"),
        supplier_id=supplier.id
    )
    
    # Ingrediente OK (Não deve aparecer)
    # Mínimo 10, Atual 15
    ing_ok = Ingredient(
        company_id=company.id,
        name="Item OK",
        unit="un",
        current_stock=Decimal("15.000"),
        min_stock_alert=Decimal("10.000"),
        supplier_id=supplier.id
    )
    
    db.add_all([ing_low, ing_ok])
    db.commit()
    db.close()

    # 3. Buscar Lista de Compras
    res = client.get("/api/admin/inventory/shopping-list", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    items = data["items"]
    
    # Validações
    # Deve conter "Item Baixo"
    found_low = next((i for i in items if i["ingredient_name"] == "Item Baixo"), None)
    assert found_low is not None
    assert float(found_low["deficit"]) == 5.0
    assert found_low["supplier_name"] == "Fornecedor Teste"
    
    # NÃO deve conter "Item OK"
    found_ok = next((i for i in items if i["ingredient_name"] == "Item OK"), None)
    assert found_ok is None