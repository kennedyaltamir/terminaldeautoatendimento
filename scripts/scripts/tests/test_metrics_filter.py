from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company
from datetime import datetime, timedelta

client = TestClient(app)

def test_metrics_date_filter():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Pedidos com datas manipuladas
    # Precisamos acessar o DB diretamente para forçar a data, pois a API usa func.now()
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Pedido HOJE (R$ 100)
    order_today = Order(
        company_id=company.id,
        table_id=1,
        total_amount=100.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now()
    )
    
    # Pedido MÊS PASSADO (R$ 200) - Fora do filtro de 7 dias
    order_old = Order(
        company_id=company.id,
        table_id=1,
        total_amount=200.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now() - timedelta(days=40)
    )
    
    db.add_all([order_today, order_old])
    db.commit()
    db.close()

    # 3. Testar Filtro "Hoje"
    today_str = datetime.now().strftime("%Y-%m-%d")
    res_today = client.get(f"/api/admin/metrics?start_date={today_str}&end_date={today_str}", headers=headers)
    assert res_today.status_code == 200
    data_today = res_today.json()
    
    # Deve contar apenas o pedido de hoje (pode haver outros do seed/testes anteriores, mas o old não deve entrar)
    # O importante é que o valor não inclua os 200 do mês passado
    # Como o banco de testes persiste, vamos verificar se o total é menor que a soma total
    
    res_all = client.get("/api/admin/metrics", headers=headers)
    total_all = float(res_all.json()["total_revenue"])
    total_today = float(data_today["total_revenue"])
    
    assert total_today < total_all
    assert total_today >= 100.00