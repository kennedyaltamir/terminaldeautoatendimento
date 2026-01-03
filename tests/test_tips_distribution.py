from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Employee, Table, TableSession, Order, OrderStatus, PaymentStatus, UserRole, ServiceFeeLedger
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_tips_calculation_and_reporting():
    """
    Testa o fluxo completo de gorjetas:
    1. Cria Garçom e Dono.
    2. Garçom abre mesa.
    3. Pedido é feito.
    4. Mesa é fechada (Cálculo de 10%).
    5. Verifica se a gorjeta foi para o Ledger.
    6. Dono verifica relatório (Acesso permitido).
    """
    # 1. Setup
    unique_slug = f"tips-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Tips Corp",
        slug=unique_slug,
        owner_email=f"tips-{uuid.uuid4().hex[:6]}@test.com",
        service_fee_percentage=Decimal("10.00")
    )
    db.add(company)
    db.commit()
    
    waiter = Employee(
        company_id=company.id,
        name="Garçom Rico",
        email=f"waiter-{uuid.uuid4().hex[:6]}@test.com",
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
    
    # Token do Garçom (Para operar a mesa)
    token_waiter = create_access_token(data={"sub": waiter.email, "role": "cashier", "account_type": "employee", "company_id": str(company.id)})
    headers_waiter = {"Authorization": f"Bearer {token_waiter}"}

    # Token do Dono (Para ver relatórios financeiros)
    token_owner = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers_owner = {"Authorization": f"Bearer {token_owner}"}
    
    db.close()

    # 2. Garçom Abre Mesa
    res_open = client.post(f"/api/admin/tables/{table_id}/open", headers=headers_waiter, json={"customer_name": "Tip Giver"})
    assert res_open.status_code == 200

    # 3. Criar Pedido (R$ 100.00)
    db = SessionLocal()
    session = db.query(TableSession).filter(TableSession.table_id == table_id, TableSession.is_active == True).first()
    assert session.opened_by_employee_id == waiter_id
    
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

    # 4. Fechar Mesa (Garçom fecha)
    res_close = client.post(f"/api/admin/tables/{table_id}/close", headers=headers_waiter, json={"payment_method": "cash"})
    assert res_close.status_code == 200

    # 5. Verificar Ledger (Banco)
    db = SessionLocal()
    ledger = db.query(ServiceFeeLedger).filter(ServiceFeeLedger.employee_id == waiter_id).first()
    assert ledger is not None
    assert ledger.amount == Decimal("10.00")
    db.close()

    # 6. Verificar Relatório (Login como Dono)
    # Aqui usamos headers_owner para evitar o 403
    res_report = client.get("/api/admin/financial/tips", headers=headers_owner)
    assert res_report.status_code == 200
    report = res_report.json()
    
    my_entry = next((r for r in report if r["employee_name"] == "Garçom Rico"), None)
    assert my_entry is not None
    assert my_entry["total_tips"] == 10.0