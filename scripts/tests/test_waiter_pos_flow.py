from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus, Employee, UserRole, Category, Product
from app.core.security import create_access_token
from decimal import Decimal
import uuid

def test_waiter_close_table_flow(client, db_session):
    """
    Testa o fluxo de fechamento de mesa pelo garçom.
    """
    # 1. Setup
    unique_slug = f"waiter-pos-{uuid.uuid4().hex[:6]}"
    company = Company(name="Waiter POS Corp", slug=unique_slug, owner_email=f"wp-{unique_slug}@test.com")
    db_session.add(company)
    db_session.commit()

    waiter = Employee(
        company_id=company.id,
        name="Garçom POS",
        email=f"pos-{unique_slug}@test.com",
        password_hash="hash",
        role=UserRole.CASHIER
    )
    db_session.add(waiter)
    db_session.commit()

    table = Table(company_id=company.id, table_number=1, qr_token="token")
    db_session.add(table)
    db_session.commit()

    cat = Category(company_id=company.id, name="Geral")
    db_session.add(cat)
    db_session.commit()
    
    prod = Product(category_id=cat.id, name="Item", price=Decimal("10.00"))
    db_session.add(prod)
    db_session.commit()

    token = create_access_token(data={"sub": waiter.email, "role": "cashier", "account_type": "employee", "company_id": str(company.id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Abrir Mesa
    open_res = client.post(f"/api/admin/tables/{table.id}/open", headers=headers, json={"customer_name": "Waiter Test"})
    assert open_res.status_code == 200

    # 3. Lançar Pedido (Staff Override)
    order_payload = {
        "table_id": table.id,
        "qr_token": "staff-override",
        "customer_name": "Waiter Test",
        "items": [{"product_id": prod.id, "quantity": 1}]
    }
    order_res = client.post(f"/api/{unique_slug}/orders", json=order_payload)
    assert order_res.status_code == 201

    # 4. Fechar Mesa
    close_res = client.post(f"/api/admin/tables/{table.id}/close", headers=headers, json={"payment_method": "cash"})
    assert close_res.status_code == 200

    # 5. Verificar Status
    db_session.refresh(table)
    # A mesa em si não tem status no banco, a sessão que tem.
    # O endpoint de dashboard calcula o status.
    dash_res = client.get("/api/admin/tables/dashboard", headers=headers)
    tables = dash_res.json()
    table_data = next(t for t in tables if t["id"] == table.id)
    assert table_data["status"] == "free"
