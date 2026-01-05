from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product, Company

client = TestClient(app)

def test_menu_returns_tags():
    """
    Verifica se o endpoint do menu retorna as tags dos produtos.
    """
    # 1. Setup: Garantir que existe um produto com tag
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    
    # Adicionar tag a um produto
    product = db.query(Product).filter(Product.category.has(company_id=company.id)).first()
    product.tags = ["promo", "novo"]
    db.commit()
    db.close()

    # 2. Buscar Menu Público
    response = client.get("/api/hamburgueria-ze/menu")
    assert response.status_code == 200
    data = response.json()

    # 3. Verificar
    found = False
    for cat in data["categories"]:
        for p in cat["products"]:
            if "promo" in p["tags"]:
                found = True
                break
    
    assert found, "Tag 'promo' não encontrada no menu"
