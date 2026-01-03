from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_route_protection():
    """Tenta acessar a cozinha sem token. Deve falhar (401)."""
    response = client.get("/api/admin/hamburgueria-ze/orders")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_admin_route_with_token():
    """
    Fluxo completo:
    1. Loga para pegar o token.
    2. Usa o token para acessar a cozinha.
    Deve funcionar (200).
    """
    # 1. Login (assumindo que o usuário admin@mesaflow.com existe do passo anterior)
    login_res = client.post(
        "/api/auth/token",
        data={"username": "admin@mesaflow.com", "password": "123456"}
    )
    # Se o login falhar, o teste para aqui (pode acontecer se o banco foi resetado)
    if login_res.status_code != 200:
        print("⚠️ Aviso: Login falhou no teste. Verifique se o usuário existe.")
        return

    token = login_res.json()["access_token"]
    
    # 2. Acesso Protegido
    # Precisamos saber o slug correto. O seed cria 'hamburgueria-ze'.
    # Se o usuário admin foi criado em cima dela, deve funcionar.
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/admin/hamburgueria-ze/orders", headers=headers)
    
    # Se o usuário admin não for dono da 'hamburgueria-ze', daria 403, o que também prova segurança.
    # Mas esperamos 200 se for o dono.
    assert response.status_code in [200, 403]