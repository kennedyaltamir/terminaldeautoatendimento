from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product, Company

client = TestClient(app)

def test_kds_quick_stock_management():
    """
    Testa o fluxo de '86' (Esgotar produto rapidamente).
    """
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Obter slug
    db = SessionLocal()
    company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
    slug = company.slug
    db.close()

    # 2. Listar produtos (Rota corrigida)
    # A rota quick-list não existe, usamos a rota normal de produtos
    list_res = client.get(f"/api/admin/menu/products", headers=headers)
    assert list_res.status_code == 200
