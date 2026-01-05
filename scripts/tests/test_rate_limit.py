from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_rate_limit_login():
    """
    Testa se o limitador bloqueia após 5 tentativas de login falhas.
    """
    # 1. Fazer 5 tentativas rápidas
    for _ in range(5):
        res = client.post(
            "/api/auth/token",
            data={"username": "hacker@test.com", "password": "123"}
        )
        # Pode ser 401 (senha errada) ou 200 (se acertar), mas não 429 ainda
        assert res.status_code != 429

    # 2. A 6ª tentativa deve ser bloqueada (429 Too Many Requests)
    res_blocked = client.post(
        "/api/auth/token",
        data={"username": "hacker@test.com", "password": "123"}
    )
    
    assert res_blocked.status_code == 429
    assert "Rate limit exceeded" in res_blocked.text