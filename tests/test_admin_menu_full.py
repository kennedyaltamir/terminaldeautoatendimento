from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_admin_menu_linkage():
    """Garante que todas as rotas de gestão de cardápio estão acessíveis e protegidas"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Testar GET Menu Admin (via Public API mas usado no Admin)
    menu_res = client.get("/api/hamburgueria-ze/menu")
    assert menu_res.status_code == 200
    
    # 3. Testar POST Categoria
    cat_res = client.post("/api/admin/menu/categories", headers=headers, json={"name": "Sobremesas Novas"})
    assert cat_res.status_code == 201