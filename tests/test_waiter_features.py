from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus
from datetime import datetime
import uuid

client = TestClient(app)

def test_waiter_session_management():
    """
    Testa as funcionalidades do App do Garçom:
    1. Renomear Sessão (Alias).
    2. Obter Detalhes da Sessão (Audit).
    """
    
    # 1. Login Admin
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup (Criar Sessão Ativa)
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    table = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    
    # Limpar sessões anteriores
    db.query(TableSession).filter(TableSession.table_id == table.id).update({"is_active": False})
    
    session = TableSession(
        company_id=company.id,
        table_id=table.id,
        customer_name="Cliente Genérico",
        session_token=str(uuid.uuid4()),
        access_pin="0000",
        is_active=True
    )
    db.add(session)
    db.commit()
    
    # Adicionar um pedido para ter valor no Audit
    order = Order(
        company_id=company.id,
        session_id=session.id,
        table_id=table.id,
        total_amount=100.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PENDING
    )
    db.add(order)
    db.commit()
    
    session_id = session.id
    db.close()

    # 3. Teste: Renomear Sessão
    new_name = "Aniversário Carol"
    rename_res = client.patch(
        f"/api/admin/tables/sessions/{session_id}", 
        headers=headers, 
        json={"customer_name": new_name}
    )
    assert rename_res.status_code == 200
    
    # 4. Teste: Obter Detalhes (Audit)
    audit_res = client.get(f"/api/admin/tables/sessions/{session_id}/details", headers=headers)
    assert audit_res.status_code == 200
    data = audit_res.json()
    
    assert data["customer_name"] == new_name
    assert float(data["total_spent"]) == 100.00
    assert len(data["orders"]) > 0