from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_menu_loading_state_contract():
    """
    Valida se o endpoint do menu responde corretamente para que o 
    frontend possa gerenciar o estado de loading/skeleton.
    """
    response = client.get("/api/hamburgueria-ze/menu")
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se a estrutura básica para renderizar o menu (ou skeleton) existe
    assert "categories" in data
    assert "company" in data
    assert isinstance(data["categories"], list)

def test_skeleton_assets_presence():
    """
    Verifica se os componentes de UI necessários para o Skeleton 
    estão mapeados no sistema de arquivos (simulação via teste de integração).
    """
    import os
    skeleton_path = "frontend/src/components/ui/Skeleton.tsx"
    menu_skeleton_path = "frontend/src/components/menu/MenuSkeleton.tsx"
    
    assert os.path.exists(skeleton_path), "Componente Skeleton base não encontrado"
    assert os.path.exists(menu_skeleton_path), "Componente MenuSkeleton não encontrado"
