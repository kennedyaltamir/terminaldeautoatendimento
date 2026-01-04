from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_smart_dispatch_recommendation():
    """
    Testa o algoritmo de recomendação de motoristas.
    Cenário:
    - Motorista A: 1 entrega ativa.
    - Motorista B: 0 entregas ativas.
    - Resultado Esperado: Motorista B deve ser o primeiro da lista.
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(name=f"Smart Corp {unique_id}", slug=f"smart-{unique_id}", owner_email=f"smart-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    driver_a = Employee(company_id=company.id, name="Driver A (Busy)", email=f"a-{unique_id}@test.com", password_hash="hash", role=UserRole.DRIVER)
    driver_b = Employee(company_id=company.id, name="Driver B (Free)", email=f"b-{unique_id}@test.com", password_hash="hash", role=UserRole.DRIVER)
    db.add_all([driver_a, driver_b])
    db.commit()
    
    # Atribuir entrega ao Driver A
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.DELIVERING,
        driver_id=driver_a.id,
        total_amount=10
    )
    db.add(order)
    db.commit()
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    driver_b_id = driver_b.id
    db.close()

    # 2. Pedir Recomendação
    res = client.get("/api/admin/delivery/recommendation", headers=headers)
    assert res.status_code == 200
    recommendations = res.json()
    
    # 3. Validar Ordem
    assert len(recommendations) == 2
    # O primeiro deve ser o Driver B (0 entregas)
    assert recommendations[0]["driver_id"] == driver_b_id
    assert recommendations[0]["active_deliveries"] == 0
    
    # O segundo deve ser o Driver A (1 entrega)
    assert recommendations[1]["active_deliveries"] == 1