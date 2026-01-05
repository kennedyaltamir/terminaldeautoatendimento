from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.database import SessionLocal
from app.models import Company

client = TestClient(app)

def test_google_auth_new_user():
    """
    Testa se o backend cria uma nova empresa ao receber um token válido
    de um e-mail ainda não cadastrado.
    """
    mock_idinfo = {
        'iss': 'accounts.google.com',
        'email': 'novo_dono@gmail.com',
        'name': 'Novo Dono Teste',
        'sub': '123456789'
    }

    with patch('google.oauth2.id_token.verify_oauth2_token', return_value=mock_idinfo):
        response = client.post("/api/auth/google", json={"credential": "TOKEN_FAKE_VALIDO"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_name"] == "Novo Dono Teste"
        assert "access_token" in data
        assert "company_slug" in data

        # Verificar se salvou no banco
        db = SessionLocal()
        company = db.query(Company).filter(Company.owner_email == "novo_dono@gmail.com").first()
        assert company is not None
        assert company.name.startswith("Loja de Novo")
        db.close()

def test_google_auth_invalid_token():
    """Testa rejeição de token malformado ou inválido."""
    with patch('google.oauth2.id_token.verify_oauth2_token', side_effect=ValueError("Invalid Token")):
        response = client.post("/api/auth/google", json={"credential": "TOKEN_LIXO"})
        assert response.status_code == 401
        assert "Google inválido" in response.json()["detail"]
