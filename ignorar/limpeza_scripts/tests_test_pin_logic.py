from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession
import uuid

client = TestClient(app)

def test_secure_pin_generation():
    """
    Valida se o PIN gerado agora possui 10 dígitos conforme solicitado.
    """
    # 1. Setup
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    table = db.query(Table).filter(Table.company_id == company.id).first()
    
    # Limpar sessões
    db.query(TableSession).filter(TableSession.table_id == table.id).update({"is_active": False})
    db.commit()
    
    # 2. Login Admin
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Abrir Mesa
    res = client.post(f"/api/admin/tables/{table.id}/open", headers=headers, json={"customer_name": "PIN Test"})
    assert res.status_code == 200
    
    data = res.json()
    pin = data["pin"]
    
    # 4. Validação
    assert len(pin) == 10
    assert pin.isdigit()
    
    print(f"✅ PIN de 10 dígitos validado: {pin}")
    db.close()
