from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Ingredient, ProductRecipe, Order, OrderStatus, PaymentStatus, Table, TableSession
from decimal import Decimal
import uuid

client = TestClient(app)

def test_full_inventory_cycle():
    """
    Teste de Integração: Ficha Técnica (Receita)
    1. Cria Ingrediente (Pão).
    2. Vincula ao Produto (X-Burger usa 1 Pão).
    3. Realiza um Pedido.
    4. Verifica se o estoque do Pão baixou.
    """
    
    # 1. Login Admin
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup do Cenário (Banco de Dados)
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Criar Ingrediente: Pão Artesanal (Estoque: 100 un)
    pao = Ingredient(
        company_id=company.id,
        name="Pão Artesanal Teste",
        unit="un",
        current_stock=100.000,
        cost_per_unit=1.50
    )
    db.add(pao)
    db.commit()
    
    # Criar Produto: X-Teste
    burger = Product(
        category_id=company.categories[0].id, # Usa a primeira categoria existente
        name="X-Teste Inventory",
        price=20.00,
        station="kitchen"
    )
    db.add(burger)
    db.commit()
    
    # Vincular Receita: 1 X-Teste gasta 1 Pão
    recipe = ProductRecipe(
        product_id=burger.id,
        ingredient_id=pao.id,
        quantity_required=1.000
    )
    db.add(recipe)
    db.commit()
    
    # IDs para verificação
    pao_id = pao.id
    burger_id = burger.id
    
    # --- CORREÇÃO: Garantir Sessão de Mesa Ativa ---
    # O sistema exige check-in. Vamos usar a Mesa 1 que já existe no seed.
    table = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    
    # Limpar sessões anteriores para evitar conflito
    db.query(TableSession).filter(TableSession.table_id == table.id).update({"is_active": False})
    
    session = TableSession(
        company_id=company.id,
        table_id=table.id,
        customer_name="QA Inventory",
        session_token=str(uuid.uuid4()),
        access_pin="1234",
        is_active=True
    )
    db.add(session)
    db.commit()
    
    db.close()

    # 3. Realizar Pedido (Vender 2 X-Teste)
    # Isso deve consumir 2 Pães (100 - 2 = 98)
    order_payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "QA Inventory",
        "payment_method": "cash",
        "items": [
            {"product_id": burger_id, "quantity": 2}
        ]
    }
    
    # Usamos o slug 'hamburgueria-ze' (padrão do seed)
    order_res = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    
    # Debug se falhar
    if order_res.status_code != 201:
        print(f"❌ Erro no pedido: {order_res.json()}")
        
    assert order_res.status_code == 201

    # 4. Verificar Baixa no Estoque
    # Consultar via API de Admin para garantir que o endpoint reflete o banco
    stock_res = client.get("/api/admin/inventory/ingredients", headers=headers)
    assert stock_res.status_code == 200
    ingredients = stock_res.json()
    
    pao_atualizado = next(i for i in ingredients if i["id"] == pao_id)
    
    # Validação
    estoque_esperado = 100.0 - 2.0
    estoque_real = float(pao_atualizado["current_stock"])
    
    assert estoque_real == estoque_esperado, f"Estoque incorreto. Esperado: {estoque_esperado}, Real: {estoque_real}"