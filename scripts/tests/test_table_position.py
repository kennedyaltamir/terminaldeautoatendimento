from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Table, Company

client = TestClient(app)

def test_update_table_positions():
    """
    Testa se o endpoint de atualização de posições funciona.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Pegar ID da Mesa 1
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    table = db.query(Table).filter(Table.company_id == company.id, Table.table_number == 1).first()
    table_id = table.id
    db.close()

    # 3. Atualizar Posição
    payload = [
        {"id": table_id, "x": 50.5, "y": 75.0}
    ]
    
    patch_res = client.patch("/api/admin/tables/positions", headers=headers, json=payload)
    assert patch_res.status_code == 200
    
    # 4. Verificar Persistência
    db = SessionLocal()
    updated_table = db.query(Table).filter(Table.id == table_id).first()
    assert float(updated_table.position_x) == 50.5
    assert float(updated_table.position_y) == 75.0
    db.close()