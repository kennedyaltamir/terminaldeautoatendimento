from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Employee, Company
import uuid

client = TestClient(app)

def test_acl_lifecycle():
    """
    Testa o ciclo de vida de permissões:
    1. Login como Dono (Owner).
    2. Dono cria um funcionário 'Cozinha'.
    3. Login como Funcionário 'Cozinha'.
    4. Funcionário tenta acessar rota restrita (Deve falhar 403).
    5. Funcionário tenta acessar rota permitida (Deve passar 200).
    """
    
    # --- SETUP: Garantir dados limpos ---
    unique_email = f"chef_{uuid.uuid4().hex[:6]}@test.com"
    
    # 1. Login como DONO (Admin)
    # (Assumindo que o seed.py já rodou e criou admin@mesaflow.com)
    login_owner = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_owner.status_code == 200
    token_owner = login_owner.json()["access_token"]
    headers_owner = {"Authorization": f"Bearer {token_owner}"}

    # 2. Dono cria Funcionário (Cozinha)
    employee_payload = {
        "name": "Mestre Cuca",
        "email": unique_email,
        "password": "senha_cozinha",
        "role": "kitchen"
    }
    
    create_res = client.post("/api/admin/employees", headers=headers_owner, json=employee_payload)
    assert create_res.status_code == 201
    assert create_res.json()["role"] == "kitchen"

    # 3. Login como FUNCIONÁRIO
    login_employee = client.post("/api/auth/token", data={"username": unique_email, "password": "senha_cozinha"})
    assert login_employee.status_code == 200
    data_employee = login_employee.json()
    
    token_employee = data_employee["access_token"]
    headers_employee = {"Authorization": f"Bearer {token_employee}"}
    
    # Validar se o token identifica corretamente o papel
    assert data_employee["user_role"] == "kitchen"

    # 4. Teste de BLOQUEIO (Rota Proibida)
    # Um cozinheiro NÃO pode criar outros funcionários
    fail_res = client.post("/api/admin/employees", headers=headers_employee, json={
        "name": "Hacker", "email": "hacker@test.com", "password": "123", "role": "manager"
    })
    
    # Esperamos 403 Forbidden
    assert fail_res.status_code == 403
    assert fail_res.json()["detail"] == "Acesso restrito a administradores"

    # 5. Teste de ACESSO (Rota Permitida)
    # Um cozinheiro DEVE conseguir ver os pedidos (KDS)
    # O slug vem no login do funcionário
    slug = data_employee["company_slug"]
    
    kds_res = client.get(f"/api/admin/{slug}/orders", headers=headers_employee)
    assert kds_res.status_code == 200
    assert isinstance(kds_res.json(), list)