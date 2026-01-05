from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_failure_wrong_password():
    """Teste de falha de login com senha incorreta"""
    response = client.post(
        "/api/auth/token",
        data={"username": "admin@mesaflow.com", "password": "senhaerrada"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha incorretos"

def test_login_failure_user_not_found():
    """Teste de falha de login com usuário inexistente"""
    response = client.post(
        "/api/auth/token",
        data={"username": "naoexiste@email.com", "password": "123"}
    )
    assert response.status_code == 401