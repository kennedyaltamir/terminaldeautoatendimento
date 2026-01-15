from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus
import uuid

client = TestClient(app)

def test_table_transfer_logic():
    """
    Testa a transferência de mesa (Move).
    1. Cria Mesa 1 (Ocupada) e Mesa 2 (Livre).
    2. Transfere Mesa 1 -> Mesa 2.
    3. Verifica se Mesa 1 ficou livre e Mesa 2 ocupada.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    
    # Garantir mesas
    t1 = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    t2 = db.query(Table).filter(Table.table_number == 2, Table.company_id == company.id).first()
    
    # Limpar sessões
    db.query(TableSession).filter(TableSession.company_id == company.id).update({"is_active": False})
    db.commit()
    
    # Ocupar Mesa 1
    session = TableSession(
        company_id=company.id, table_id=t1.id, customer_name="Transfer Test",
        session_token=str(uuid.uuid4()), access_pin="0000", is_active=True
    )
    db.add(session)
    db.commit()
    
    t1_id = t1.id
    t2_id = t2.id
    db.close()

    # 3. Transferir
    payload = {"from_table_id": t1_id, "to_table_id": t2_id, "merge": False}
    res = client.post("/api/admin/tables/transfer", headers=headers, json=payload)
    assert res.status_code == 200
    assert "Transferido" in res.json()["message"]

    # 4. Verificar Estado
    dash_res = client.get("/api/admin/tables/dashboard", headers=headers)
    tables = dash_res.json()
    
    table1_data = next(t for t in tables if t["id"] == t1_id)
    table2_data = next(t for t in tables if t["id"] == t2_id)
    
    assert table1_data["status"] == "free"
    assert table2_data["status"] == "occupied"
    assert table2_data["active_session"]["customer_name"] == "Transfer Test"

def test_table_merge_logic():
    """
    Testa a junção de mesas (Merge).
    1. Cria Mesa 1 (Ocupada) e Mesa 2 (Ocupada).
    2. Tenta transferir sem flag merge -> Falha (409).
    3. Transfere com flag merge -> Sucesso.
    4. Verifica se pedidos foram unificados.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    t1 = db.query(Table).filter(Table.table_number == 1, Table.company_id == company.id).first()
    t2 = db.query(Table).filter(Table.table_number == 2, Table.company_id == company.id).first()
    
    # Limpar
    db.query(TableSession).filter(TableSession.company_id == company.id).update({"is_active": False})
    db.commit()
    
    # Ocupar ambas
    s1 = TableSession(company_id=company.id, table_id=t1.id, customer_name="Mesa 1", session_token=str(uuid.uuid4()), access_pin="0000", is_active=True)
    s2 = TableSession(company_id=company.id, table_id=t2.id, customer_name="Mesa 2", session_token=str(uuid.uuid4()), access_pin="0000", is_active=True)
    db.add_all([s1, s2])
    db.commit()
    
    # Adicionar pedidos
    o1 = Order(company_id=company.id, session_id=s1.id, table_id=t1.id, total_amount=10, status=OrderStatus.PENDING)
    o2 = Order(company_id=company.id, session_id=s2.id, table_id=t2.id, total_amount=20, status=OrderStatus.PENDING)
    db.add_all([o1, o2])
    db.commit()
    
    t1_id = t1.id
    t2_id = t2.id
    db.close()

    # 3. Tentar Transferir (Sem Merge) -> Deve falhar
    payload = {"from_table_id": t1_id, "to_table_id": t2_id, "merge": False}
    res_fail = client.post("/api/admin/tables/transfer", headers=headers, json=payload)
    assert res_fail.status_code == 409

    # 4. Transferir (Com Merge)
    payload["merge"] = True
    res_ok = client.post("/api/admin/tables/transfer", headers=headers, json=payload)
    assert res_ok.status_code == 200
    assert "unificadas" in res_ok.json()["message"]

    # 5. Verificar
    dash_res = client.get("/api/admin/tables/dashboard", headers=headers)
    tables = dash_res.json()
    
    t1_data = next(t for t in tables if t["id"] == t1_id)
    t2_data = next(t for t in tables if t["id"] == t2_id)
    
    assert t1_data["status"] == "free"
    assert t2_data["status"] == "occupied"
    # Total deve ser 30 (10 + 20)
    assert float(t2_data["active_session"]["total_spent"]) == 30.00