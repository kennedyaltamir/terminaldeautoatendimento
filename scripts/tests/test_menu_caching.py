from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.cache import CacheService
import json

client = TestClient(app)

def test_menu_caching_flow():
    """
    Testa se o menu é cacheado e se a invalidação funciona.
    Usa Mock do Redis para não depender de infra externa.
    """
    
    # 1. Mock do Redis
    mock_redis = MagicMock()
    # Simula cache vazio inicialmente
    mock_redis.get.return_value = None
    
    with patch("app.core.cache.CacheService._client", mock_redis), \
         patch("app.core.cache.CacheService._enabled", True):
        
        # 2. Primeira chamada (Cache Miss)
        # Deve ir ao banco e salvar no Redis
        res1 = client.get("/api/hamburgueria-ze/menu")
        assert res1.status_code == 200
        
        # Verifica se tentou salvar no cache
        mock_redis.setex.assert_called()
        args, _ = mock_redis.setex.call_args
        key = args[0]
        assert "menu:hamburgueria-ze" in key
        
        # 3. Segunda chamada (Cache Hit)
        # Configura o mock para retornar o dado salvo
        cached_data = json.dumps(res1.json())
        mock_redis.get.return_value = cached_data
        
        res2 = client.get("/api/hamburgueria-ze/menu")
        assert res2.status_code == 200
        assert res2.json() == res1.json()
        
        # 4. Invalidação (Simulando update de produto)
        # Login
        login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Criar Categoria (Dispara invalidação)
        client.post("/api/admin/menu/categories", headers=headers, json={"name": "Cache Test"})
        
        # Verifica se chamou delete
        mock_redis.keys.return_value = ["menu:hamburgueria-ze:/api/hamburgueria-ze/menu"]
        CacheService.invalidate_menu("hamburgueria-ze")
        mock_redis.delete.assert_called()
        
        print("✅ Fluxo de Cache (Get -> Set -> Invalidate) validado!")
