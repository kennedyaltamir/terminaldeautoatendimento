from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Order, OrderStatus, PaymentStatus, Company
from datetime import datetime, timedelta

client = TestClient(app)

def test_advanced_metrics_aggregation():
    """
    Testa se as novas métricas (Vendas por Hora, Ticket Médio) estão sendo calculadas.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Pedidos em horários diferentes
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Pedido às 12:00
    order_lunch = Order(
        company_id=company.id,
        table_id=1,
        total_amount=50.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    )
    
    # Pedido às 20:00
    order_dinner = Order(
        company_id=company.id,
        table_id=1,
        total_amount=100.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
    )
    
    db.add_all([order_lunch, order_dinner])
    db.commit()
    db.close()

    # 3. Buscar Métricas
    res = client.get("/api/admin/metrics?start_date=" + datetime.now().strftime("%Y-%m-%d"), headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # 4. Validar Vendas por Hora
    hours = [item["hour"] for item in data["sales_by_hour"]]
    assert 12 in hours
    assert 20 in hours
    
    # 5. Validar Ticket Médio
    # CORREÇÃO: Converter para float antes de comparar, pois Decimal vem como string no JSON
    assert len(data["ticket_evolution"]) > 0
    assert float(data["average_ticket"]) > 0