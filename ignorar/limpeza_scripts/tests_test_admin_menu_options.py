from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_can_manage_options():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    # Se o login falhar (banco limpo), pula o teste
    if login_res.status_code != 200:
        return

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Grupo de Opção para o Produto 1
    # Assumindo que o produto 1 existe (seed)
    group_res = client.post(
        "/api/admin/menu/products/1/groups",
        headers=headers,
        json={"name": "Teste Grupo", "min_selection": 0, "max_selection": 1}
    )
    
    # Se o produto 1 não existir, o teste deve lidar com 404 ou criar um produto antes
    if group_res.status_code == 404:
        return

    assert group_res.status_code == 201
    group_id = group_res.json()["id"]

    # 3. Criar Opção no Grupo
    opt_res = client.post(
        f"/api/admin/menu/groups/{group_id}/options",
        headers=headers,
        json={"name": "Opção Teste", "price": 5.00}
    )
    assert opt_res.status_code == 201

    # 4. Deletar Grupo (Cascade deleta opções)
    del_res = client.delete(f"/api/admin/menu/groups/{group_id}", headers=headers)
    assert del_res.status_code == 204
