from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Employee, UserRole, PaymentMethod, DriverLedger, LedgerType
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_driver_finance_flow():
    """
    Testa o fluxo financeiro completo do motorista:
    1. Acúmulo de dívida (Entrega em dinheiro).
    2. Verificação de saldo.
    3. Pagamento da dívida (Settlement).
    4. Verificação de saldo zerado.
    """
    # --- FASE 1: ACÚMULO DE DÍVIDA ---
    
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(name=f"Log Fin {unique_id}", slug=f"logfin-{unique_id}", owner_email=f"logfin-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    driver = Employee(
        company_id=company.id,
        name=f"Driver {unique_id}", # Nome único para evitar colisão
        email=f"debt-{unique_id}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(driver)
    db.commit()
    
    # Pedido em Dinheiro (R$ 50)
    order = Order(
        company_id=company.id,
        order_type=OrderType.DELIVERY,
        status=OrderStatus.DELIVERING,
        payment_method=PaymentMethod.CASH,
        total_amount=Decimal("50.00"),
        driver_id=driver.id
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    driver_id = driver.id
    
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Finalizar Entrega (Gera Dívida)
    res = client.patch(f"/api/admin/delivery/orders/{order_id}/complete", headers=headers)
    assert res.status_code == 200

    # 3. Verificar Ledger no Banco
    db = SessionLocal()
    ledger = db.query(DriverLedger).filter(DriverLedger.driver_id == driver_id).first()
    assert ledger is not None
    assert ledger.type == LedgerType.DEBT
    assert ledger.amount == Decimal("50.00")
    db.close()

    # 4. Verificar Saldo via API (Deve ser 50.00)
    res_balance = client.get(f"/api/admin/logistics/drivers/{driver_id}/balance", headers=headers)
    assert res_balance.status_code == 200
    assert float(res_balance.json()["current_debt"]) == 50.00

    # --- FASE 2: PAGAMENTO DA DÍVIDA ---

    # 5. Pagar R$ 50 (Settlement)
    payload = {"amount": 50.00, "description": "Acerto do dia"}
    res_settle = client.post(f"/api/admin/logistics/drivers/{driver_id}/settle", headers=headers, json=payload)
    assert res_settle.status_code == 200

    # 6. Verificar Saldo Zerado
    res_balance_final = client.get(f"/api/admin/logistics/drivers/{driver_id}/balance", headers=headers)
    assert float(res_balance_final.json()["current_debt"]) == 0.00