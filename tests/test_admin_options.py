from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_option_group_and_option():
    """Valida se o admin consegue criar grupos de opções e opções para um produto"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_res.status_code == 200, f"Login falhou: {login_res.text}"
    
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Grupo de Opção para o Produto 1 (X-Bacon do seed)
    group_payload = {"name": "Extras Teste", "min_selection": 0, "max_selection": 3}
    response = client.post("/api/admin/menu/products/1/groups", headers=headers, json=group_payload)
    assert response.status_code == 201
    group_id = response.json()["id"]

    # 3. Criar Opção dentro do grupo
    option_payload = {"name": "Cheddar Teste", "price": 4.50}
    response = client.post(f"/api/admin/menu/groups/{group_id}/options", headers=headers, json=option_payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Cheddar Teste"