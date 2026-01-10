import sys
import os

# Adiciona o diretório raiz ao path para permitir importação de 'app'
# scripts/tests/test_mobile_auth.py -> sobe 3 níveis -> raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Employee, UserRole, UserDevice
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_mobile_device_registration_flow():
    """
    Testa o fluxo de registro de dispositivo móvel para Push Notifications.
    1. Cria Empresa e Funcionário.
    2. Funcionário registra dispositivo (FCM Token).
    3. Verifica persistência no banco.
    4. Funcionário faz logout (remove dispositivo).
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()

    company = Company(
        name=f"Mobile Corp {unique_id}",
        slug=f"mob-{unique_id}",
        owner_email=f"mob-{unique_id}@test.com"
    )
    db.add(company)
    db.commit()

    employee = Employee(
        company_id=company.id,
        name="Mobile User",
        email=f"user-{unique_id}@test.com",
        password_hash="hash",
        role=UserRole.DRIVER
    )
    db.add(employee)
    db.commit()

    emp_id = employee.id
    company_id = company.id

    # Token de Funcionário
    token = create_access_token(data={"sub": employee.email, "role": "driver", "account_type": "employee", "company_id": str(company.id)})
    headers = {"Authorization": f"Bearer {token}"}

    db.close()

    # 2. Registrar Dispositivo
    fcm_token = f"fcm-token-{unique_id}"
    payload = {
        "fcm_token": fcm_token,
        "device_name": "Samsung S24",
        "platform": "android"
    }

    res_reg = client.post("/api/auth/device", headers=headers, json=payload)
    assert res_reg.status_code == 200
    assert res_reg.json()["message"] == "Dispositivo registrado com sucesso"

    # 3. Verificar Banco
    db = SessionLocal()
    device = db.query(UserDevice).filter(UserDevice.fcm_token == fcm_token).first()
    assert device is not None
    assert device.employee_id == emp_id
    assert device.platform == "android"
    db.close()

    # 4. Remover Dispositivo (Logout)
    res_del = client.delete(f"/api/auth/device/{fcm_token}", headers=headers)
    assert res_del.status_code == 204

    # Verificar Remoção
    db = SessionLocal()
    device_deleted = db.query(UserDevice).filter(UserDevice.fcm_token == fcm_token).first()
    assert device_deleted is None
    db.close()

    print("✅ Fluxo Mobile Auth validado!")

if __name__ == "__main__":
    test_mobile_device_registration_flow()
