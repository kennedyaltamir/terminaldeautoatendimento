from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_menu_structure_with_options():
    """Verifica se o cardápio público retorna a estrutura de opções corretamente"""
    response = client.get("/api/hamburgueria-ze/menu")
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se categorias existem
    assert "categories" in data
    # Verifica se o primeiro produto tem grupos de opções (conforme seed)
    if data["categories"][0]["products"]:
        product = data["categories"][0]["products"][0]
        assert "option_groups" in product