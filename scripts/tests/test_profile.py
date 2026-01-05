from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_password_update_flow():
    # 1. Login Inicial (Senha padrão do seed: 123456)
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Tentar mudar senha com senha atual errada
    wrong_payload = {"current_password": "senha_errada_123", "new_password": "newpassword123"}
    response = client.patch("/api/admin/company/me/password", headers=headers, json=wrong_payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "A senha atual está incorreta"

    # 3. Mudar senha com sucesso
    success_payload = {"current_password": "123456", "new_password": "newpassword123"}
    response = client.patch("/api/admin/company/me/password", headers=headers, json=success_payload)
    assert response.status_code == 200

    # 4. Verificar login com a NOVA senha
    login_new = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "newpassword123"})
    assert login_new.status_code == 200
    new_token = login_new.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}

    # 5. Reverter senha para o padrão (para não quebrar outros testes)
    revert_payload = {"current_password": "newpassword123", "new_password": "123456"}
    response = client.patch("/api/admin/company/me/password", headers=new_headers, json=revert_payload)
    assert response.status_code == 200