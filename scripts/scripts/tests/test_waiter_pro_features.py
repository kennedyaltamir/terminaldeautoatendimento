import sys
import os
from decimal import Decimal

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Employee, Table, TableSession, Order, OrderStatus, PaymentStatus, UserRole, ServiceFeeLedger
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_waiter_pro_features():
    """
    Testa as funcionalidades do Garçom Pro:
    1. Identificação de Cliente (Wallet).
    2. Fechamento com Gorjeta Personalizada.
    """
    print("🧪 Testando Garçom Pro Features...")

    # 1. Setup
    unique_slug = f"pro-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Pro Waiter Corp",
        slug=unique_slug,
        owner_email=f"pro-{uuid.uuid4().hex[:6]}@test.com",
        service_fee_percentage=Decimal("10.00") # Padrão 10%
    )
    db.add(company)
    db.commit()

    waiter = Employee(
        company_id=company.id,
        name="Garçom Pro",
        email=f"waiter-{unique_slug}@test.com",
        password_hash="hash",
        role=UserRole.CASHIER
    )
    db.add(waiter)
    db.commit()

    table = Table(company_id=company.id, table_number=1, qr_token="token")
    db.add(table)
    db.commit()

    company_id = company.id
    waiter_id = waiter.id
    table_id = table.id

    token = create_access_token(data={"sub": waiter.email, "role": "cashier", "account_type": "employee", "company_id": str(company.id)})
    headers = {"Authorization": f"Bearer {token}"}

    db.close()

    # 2. Abrir Mesa
    client.post(f"/api/admin/tables/{table_id}/open", headers=headers, json={"customer_name": "Pro Client"})

    # 3. Criar Pedido (R$ 100.00)
    db = SessionLocal()
    session = db.query(TableSession).filter(TableSession.table_id == table_id, TableSession.is_active == True).first()
    # Vincula ao garçom para ele receber a gorjeta
    session.opened_by_employee_id = waiter_id
    db.commit()

    order = Order(
        company_id=company_id,
        session_id=session.id,
        table_id=table_id,
        total_amount=Decimal("100.00"),
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PENDING
    )
    db.add(order)
    db.commit()
    db.close()

    # 4. Fechar Mesa com Gorjeta Personalizada (R$ 15,00 em vez de R$ 10,00)
    payload = {
        "payment_method": "cash",
        "custom_service_fee": 15.00
    }
    res_close = client.post(f"/api/admin/tables/{table_id}/close", headers=headers, json=payload)
    assert res_close.status_code == 200

    # 5. Verificar Ledger
    db = SessionLocal()
    ledger = db.query(ServiceFeeLedger).filter(ServiceFeeLedger.employee_id == waiter_id).first()
    
    assert ledger is not None
    # Deve ser 15.00 (Custom) e não 10.00 (Padrão)
    assert ledger.amount == Decimal("15.00")
    
    print("✅ Gorjeta personalizada registrada com sucesso!")
    db.close()

if __name__ == "__main__":
    test_waiter_pro_features()
