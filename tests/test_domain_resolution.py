from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
import uuid

client = TestClient(app)

def test_domain_resolution_flow():
    """
    Testa se o backend resolve corretamente um domínio customizado para um slug.
    """
    # 1. Setup
    unique_slug = f"domain-test-{uuid.uuid4().hex[:6]}"
    custom_domain = f"loja-{uuid.uuid4().hex[:6]}.local"
    
    db = SessionLocal()
    company = Company(
        name="Domain Corp",
        slug=unique_slug,
        owner_email=f"domain-{uuid.uuid4().hex[:6]}@test.com",
        custom_domain=custom_domain
    )
    db.add(company)
    db.commit()
    db.close()

    # 2. Testar Resolução (Sucesso)
    res = client.get(f"/api/resolve-domain?host={custom_domain}")
    assert res.status_code == 200
    assert res.json()["slug"] == unique_slug
    assert res.json()["valid"] is True

    # 3. Testar Resolução (Falha)
    res_fail = client.get("/api/resolve-domain?host=nao-existe.com")
    assert res_fail.status_code == 404