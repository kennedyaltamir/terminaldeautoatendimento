from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession
import uuid

client = TestClient(app)

def test_pin_visibility_in_dashboard():
    """
    Garante que o access_pin de 10 dígitos é retornado no dashboard administrativo.
    """
    # 1. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    table = db.query(Table).filter(Table.company_id == company.id).first()
    
    # Limpar sessões ativas para evitar conflito
    db.query(TableSession).filter(TableSession.table_id == table.id).update({"is_active": False})
    db.commit()
    
    # 2. Login Admin
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Abrir Mesa (Gera PIN de 10 dígitos)
    open_res = client.post(f"/api/admin/tables/{table.id}/open", headers=headers, json={"customer_name": "Visibility Test"})
    assert open_res.status_code == 200
    generated_pin = open_res.json()["pin"]
    assert len(generated_pin) == 10

    # 4. Consultar Dashboard
    dash_res = client.get("/api/admin/tables/dashboard", headers=headers)
    assert dash_res.status_code == 200
    
    data = dash_res.json()
    # Encontra a mesa que acabamos de abrir
    target_table = next((t for t in data if t["id"] == table.id), None)
    
    # 5. Validação Crítica: O campo access_pin deve estar presente no JSON
    assert target_table is not None
    assert target_table["active_session"] is not None
    assert "access_pin" in target_table["active_session"]
    assert target_table["active_session"]["access_pin"] == generated_pin
    
    print(f"✅ Sucesso: Token {generated_pin} visível no dashboard!")
    db.close()
