from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_settings_validation():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Teste Cor Inválida (Backend)
    invalid_color = {"primary_color": "AZUL-CLARO"}
    res_bad = client.patch("/api/admin/company/me", headers=headers, json=invalid_color)
    assert res_bad.status_code == 422 # Unprocessable Entity
    
    # 3. Teste Cor Válida
    valid_color = {"primary_color": "#FF5733"}
    res_good = client.patch("/api/admin/company/me", headers=headers, json=valid_color)
    assert res_good.status_code == 200
    assert res_good.json()["primary_color"] == "#FF5733"

    # 4. Teste URL Inválida (Pydantic padrão aceita string, mas o frontend valida URL. 
    # O backend definimos como String(500) opcional. Se quiséssemos validar URL no backend,
    # teríamos que usar HttpUrl no Pydantic, mas por compatibilidade com dados legados,
    # mantivemos string no schema backend atual para evitar quebra de migração, 
    # focando a validação forte no frontend e regex de cor no backend.)