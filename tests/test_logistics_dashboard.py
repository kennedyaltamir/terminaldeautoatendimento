from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole, DriverLedger, LedgerType
from app.core.security import create_access_token
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

client = TestClient(app)

def test_logistics_dashboard_metrics():
    """
    Testa se o dashboard de logística calcula corretamente os KPIs.
    Cenário:
    1. 1 Motorista Ativo.
    2. 2 Entregas Finalizadas (uma rápida, uma lenta).
    3. 1 Entrega Pendente.
    4. R$ 50,00 arrecadados em dinheiro.
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(name=f"Log Dash {unique_id}", slug=f"logdash-{unique_id}", owner_email=f"logdash-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    driver = Employee(
        company_id=company.id,
        name="Speedy Driver",
        email=f"speedy-{unique_id}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver)
    db.commit()
    
    # Pedido 1: Finalizado (Rápido - 10 min)
    now = datetime.now()
    order1 = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.DELIVERED,
        driver_id=driver.id,
        total_amount=Decimal("50.00"),
        created_at=now - timedelta(minutes=20),
        finished_at=now - timedelta(minutes=10)
    )
    
    # Pedido 2: Finalizado (Lento - 50 min)
    order2 = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.DELIVERED,
        driver_id=driver.id,
        total_amount=Decimal("30.00"),
        created_at=now - timedelta(minutes=60),
        finished_at=now - timedelta(minutes=10)
    )
    
    # Pedido 3: Pendente (Em Rota)
    order3 = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.DELIVERING,
        driver_id=driver.id,
        total_amount=Decimal("40.00"),
        created_at=now
    )
    
    db.add_all([order1, order2, order3])
    db.commit()
    
    # Ledger: Motorista recebeu R$ 50 do Pedido 1
    ledger = DriverLedger(
        company_id=company.id,
        driver_id=driver.id,
        order_id=order1.id,
        type=LedgerType.DEBT,
        amount=Decimal("50.00"),
        description="Cash"
    )
    db.add(ledger)
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Request Dashboard
    res = client.get("/api/admin/logistics/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # 3. Validações
    assert data["active_drivers"] == 1
    assert data["deliveries_today"] == 2
    assert data["pending_deliveries"] == 1
    
    # Tempo Médio: (10 min + 50 min) / 2 = 30 min
    # Pode haver pequena variação de segundos, aceitamos margem
    assert 29 <= data["average_delivery_time_minutes"] <= 31
    
    assert data["total_collected_cash"] == 50.00
    assert data["top_driver"] == "Speedy Driver"