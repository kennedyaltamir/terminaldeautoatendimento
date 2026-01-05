from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product, Company

client = TestClient(app)

def test_kds_quick_stock_management():
    """
    Testa o fluxo de '86' (Esgotar produto rapidamente):
    1. Listar produtos via endpoint rápido.
    2. Alternar disponibilidade de um produto.
    3. Verificar se o produto ficou indisponível.
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Listar produtos (Quick List)
    list_res = client.get("/api/admin/hamburgueria-ze/products/quick-list", headers=headers)
    assert list_res.status_code == 200
    products = list_res.json()
    assert len(products) > 0
    
    target_product = products[0]
    original_status = target_product["is_available"]
    
    # 3. Alternar status (Toggle)
    patch_res = client.patch(
        f"/api/admin/menu/products/{target_product['id']}",
        headers=headers,
        json={"is_available": not original_status}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["is_available"] != original_status
    
    # 4. Verificar persistência
    db = SessionLocal()
    db_prod = db.query(Product).filter(Product.id == target_product["id"]).first()
    assert db_prod.is_available != original_status
    db.close()
    
    # Reverter para não quebrar outros testes
    client.patch(
        f"/api/admin/menu/products/{target_product['id']}",
        headers=headers,
        json={"is_available": original_status}
    )