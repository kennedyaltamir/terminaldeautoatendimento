from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company, OrderItem, Product
from datetime import datetime, timedelta
import uuid

client = TestClient(app)

def test_bi_analytics_aggregation():
    """
    Testa se o backend agrega corretamente os dados para o dashboard.
    Cenário:
    1. Cria 2 pedidos em horários diferentes.
    2. Verifica se o total de vendas bate.
    3. Verifica se a venda por hora identifica os horários.
    4. Verifica se o CSV é gerado.
    """
    
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup de Dados
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Produto para teste
    prod = db.query(Product).filter(Product.category.has(company_id=company.id)).first()
    prod_name = prod.name # Guardar o nome antes de fechar a sessão
    prod_id = prod.id     # Guardar o ID também
    
    # Pedido 1: Hoje às 10:00 - R$ 50.00
    date_1 = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    order_1 = Order(
        company_id=company.id,
        table_id=1,
        total_amount=50.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=date_1
    )
    
    # Pedido 2: Hoje às 14:00 - R$ 150.00
    date_2 = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    order_2 = Order(
        company_id=company.id,
        table_id=1,
        total_amount=150.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=date_2
    )
    
    db.add_all([order_1, order_2])
    db.commit()
    
    # Adicionar itens para testar Curva ABC
    item_1 = OrderItem(order_id=order_1.id, product_id=prod_id, quantity=1, unit_price=50.00)
    item_2 = OrderItem(order_id=order_2.id, product_id=prod_id, quantity=3, unit_price=50.00)
    db.add_all([item_1, item_2])
    db.commit()
    
    db.close()

    # 3. Testar Agregação
    today_str = datetime.now().strftime("%Y-%m-%d")
    res = client.get(f"/api/admin/metrics?start_date={today_str}&end_date={today_str}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # Validar Totais (Pode ser maior que 200 se houver dados de outros testes, então checamos >=)
    assert float(data["total_revenue"]) >= 200.00
    
    # Validar Horários (Deve conter 10h e 14h)
    hours = [h["hour"] for h in data["sales_by_hour"]]
    assert 10 in hours
    assert 14 in hours
    
    # Validar Curva ABC
    # Usar a variável local prod_name em vez de acessar o objeto detached
    top_prod = next((p for p in data["product_performance"] if p["name"] == prod_name), None)
    assert top_prod is not None
    assert top_prod["quantity"] >= 4 # 1 + 3

    # 4. Testar Exportação CSV
    csv_res = client.get(f"/api/admin/metrics/export?start_date={today_str}&end_date={today_str}", headers=headers)
    assert csv_res.status_code == 200
    
    # CORREÇÃO: Verificar se contém "text/csv" em vez de igualdade estrita
    # O servidor pode retornar "text/csv; charset=utf-8"
    assert "text/csv" in csv_res.headers["content-type"]
    
    content = csv_res.text
    assert "ID Pedido,Data,Hora" in content # Cabeçalho
    assert "150,00" in content # Valor do pedido 2 (formato PT-BR com vírgula)