from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_menu_returns_tags():
    """
    Verifica se o endpoint do menu retorna as tags dos produtos.
    Isso é essencial para o funcionamento do filtro de tags no frontend.
    """
    # 1. Buscar Menu Público
    response = client.get("/api/hamburgueria-ze/menu")
    assert response.status_code == 200
    data = response.json()
    
    # 2. Verificar se produtos têm tags
    # O seed adicionou tags ao X-Bacon, Coca e Batata
    
    # Encontrar X-Bacon
    xbacon = next(p for cat in data["categories"] for p in cat["products"] if p["name"] == "X-Bacon")
    assert "tags" in xbacon
    assert "promo" in xbacon["tags"]
    assert "carne" in xbacon["tags"]
    
    # Encontrar Batata
    batata = next(p for cat in data["categories"] for p in cat["products"] if p["name"] == "Batata Frita")
    assert "vegano" in batata["tags"]