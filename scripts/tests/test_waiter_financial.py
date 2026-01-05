from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus, Employee, UserRole
from app.core.security import create_access_token
from decimal import Decimal
import uuid

def test_waiter_close_table_with_cash(client, db_session):
    """
    Testa o fluxo financeiro do garçom:
    1. Abre mesa.
    2. Faz pedido.
    3. Fecha mesa com dinheiro.
    """
    # 1. Setup
    unique_slug = f"waiter-fin-{uuid.uuid4().hex[:6]}"
    company = Company(name="Waiter Fin Corp", slug=unique_slug, owner_email=f"wf-{unique_slug}@test.com")
    db_session.add(company)
    db_session.commit()

    waiter = Employee(
        company_id=company.id,
        name="Garçom Teste",
        email=f"waiter-{unique_slug}@test.com",
        password_hash="hash",
        role=UserRole.CASHIER
    )
    db_session.add(waiter)
    db_session.commit()

    table = Table(company_id=company.id, table_number=1, qr_token="token")
    db_session.add(table)
    db_session.commit()

    # Token do Garçom
    token = create_access_token(data={"sub": waiter.email, "role": "cashier", "account_type": "employee", "company_id": str(company.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Abrir Mesa
    client.post(f"/api/admin/tables/{table.id}/open", headers=headers, json={"customer_name": "Cash Payer"})
    
    # Recuperar sessão
    session = db_session.query(TableSession).filter(TableSession.table_id == table.id, TableSession.is_active == True).first()

    # 3. Pedido Pendente
    order = Order(
        company_id=company.id,
        session_id=session.id,
        table_id=table.id,
        total_amount=Decimal("50.00"),
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PENDING
    )
    db_session.add(order)
    db_session.commit()
    order_id = str(order.id)

    # 4. Fechar Mesa (Pagamento em Dinheiro)
    close_res = client.post(
        f"/api/admin/tables/{table.id}/close", 
        headers=headers, 
        json={"payment_method": "cash"}
    )
    assert close_res.status_code == 200

    # 5. Verificar se o pedido foi pago
    db_session.refresh(order)
    assert order.payment_status == PaymentStatus.PAID
    
    # Verificar se a mesa foi liberada
    db_session.refresh(session)
    assert session.is_active is False
