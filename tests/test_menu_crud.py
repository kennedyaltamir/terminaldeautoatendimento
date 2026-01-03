from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_menu_management_flow():
    """
    Testa o ciclo de vida do cardápio:
    1. Login (Admin)
    2. Criar Categoria
    3. Criar Produto
    4. Editar Preço
    5. Deletar Produto
    """
    # 1. Login
    login_res = client.post(
        "/api/auth/token",
        data={"username": "admin@mesaflow.com", "password": "123456"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar Categoria "Promoções"
    cat_res = client.post(
        "/api/admin/menu/categories",
        headers=headers,
        json={"name": "Promoções", "order_index": 0}
    )
    assert cat_res.status_code == 201
    cat_id = cat_res.json()["id"]

    # 3. Criar Produto "Combo Teste"
    prod_res = client.post(
        "/api/admin/menu/products",
        headers=headers,
        json={
            "category_id": cat_id,
            "name": "Combo Teste",
            "price": 19.90,
            "is_available": True
        }
    )
    assert prod_res.status_code == 201
    prod_id = prod_res.json()["id"]
    assert prod_res.json()["price"] == "19.90"

    # 4. Editar Preço para 25.00
    patch_res = client.patch(
        f"/api/admin/menu/products/{prod_id}",
        headers=headers,
        json={"price": 25.00}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["price"] == "25.00"

    # 5. Deletar Produto
    del_res = client.delete(
        f"/api/admin/menu/products/{prod_id}",
        headers=headers
    )
    assert del_res.status_code == 204