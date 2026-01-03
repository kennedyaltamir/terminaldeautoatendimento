from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Ingredient, Product, Company, TableSession, Table
from decimal import Decimal
import uuid

client = TestClient(app)

def test_recipe_deduction():
    """
    Testa se ao vender um produto, os ingredientes da ficha técnica são baixados.
    Cenário:
    1. Verifica estoque inicial.
    2. Abre sessão na mesa (Check-in).
    3. Faz pedido.
    4. Verifica baixa no estoque.
    """
    # 1. Login (apenas para garantir token se precisar no futuro)
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]

    # 2. Setup do Banco de Dados
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Verificar estoque inicial da Carne (10kg)
    carne = db.query(Ingredient).filter(Ingredient.name == "Carne Moída", Ingredient.company_id == company.id).first()
    initial_stock = float(carne.current_stock)
    assert initial_stock == 10.000
    
    # Pegar ID do X-Bacon
    xbacon = db.query(Product).filter(Product.name == "X-Bacon", Product.category.has(company_id=company.id)).first()
    xbacon_id = xbacon.id
    
    # Pegar a Mesa 1
    table = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    
    # Extrair dados antes de fechar a sessão ou usar o objeto
    table_id = table.id
    table_qr = table.qr_token
    company_id = company.id
    
    # --- CORREÇÃO: CRIAR SESSÃO DE MESA ATIVA ---
    # O sistema exige check-in para pedidos na mesa. Vamos simular isso no banco.
    active_session = TableSession(
        company_id=company_id,
        table_id=table_id,
        customer_name="Stock Tester",
        session_token=str(uuid.uuid4()),
        access_pin="1234",
        is_active=True
    )
    db.add(active_session)
    db.commit()
    
    db.close() # Agora podemos fechar, pois já temos os IDs

    # 3. Vender 2 X-Bacon
    # Receita: 0.180kg por unidade -> Total 0.360kg
    order_payload = {
        "table_id": table_id,
        "qr_token": table_qr,
        "customer_name": "Stock Tester",
        "items": [{"product_id": xbacon_id, "quantity": 2}]
    }
    
    res_order = client.post("/api/hamburgueria-ze/orders", json=order_payload)
    
    # Debug caso falhe novamente
    if res_order.status_code != 201:
        print(f"❌ Erro no pedido: {res_order.json()}")
        
    assert res_order.status_code == 201

    # 4. Verificar estoque final
    db = SessionLocal()
    carne_updated = db.query(Ingredient).filter(Ingredient.name == "Carne Moída").first()
    expected_stock = initial_stock - (0.180 * 2)
    
    # Usar float para comparação simples
    assert float(carne_updated.current_stock) == expected_stock
    
    db.close()