from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Lead

client = TestClient(app)

def test_lead_capture():
    """
    Testa se o endpoint de captura de leads funciona e salva no banco.
    """
    # 1. Enviar Lead
    payload = {"email": "lead@test.com", "source": "test_script"}
    res = client.post("/api/leads", json=payload)
    
    assert res.status_code == 201
    assert "download_url" in res.json()

    # 2. Verificar Banco
    db = SessionLocal()
    lead = db.query(Lead).filter(Lead.email == "lead@test.com").first()
    assert lead is not None
    assert lead.source == "test_script"
    db.close()