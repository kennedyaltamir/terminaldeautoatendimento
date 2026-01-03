from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_menu_returns_categories_with_ids():
    """
    Verifica se o endpoint do menu retorna categorias com IDs.
    Isso é essencial para o funcionamento do Scroll Spy e Sticky Nav no frontend.
    """
    # 1. Buscar Menu Público
    response = client.get("/api/hamburgueria-ze/menu")
    assert response.status_code == 200
    data = response.json()
    
    # 2. Verificar estrutura
    assert "categories" in data
    assert len(data["categories"]) > 0
    
    first_cat = data["categories"][0]
    
    # 3. Validar campos necessários para o Nav
    assert "id" in first_cat
    assert "name" in first_cat
    assert isinstance(first_cat["id"], int)
    assert isinstance(first_cat["name"], str)
    
    # O frontend usa activeId={cat.id} e data-id={cat.id}
    # Se o ID não for inteiro ou não existir, o scroll spy quebra.