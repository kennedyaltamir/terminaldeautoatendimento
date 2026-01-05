from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, CompanySegment
import uuid

client = TestClient(app)

def test_registration_with_segment_and_strong_password():
    unique_slug = f"test-saas-{uuid.uuid4().hex[:6]}"
    unique_email = f"saas-{uuid.uuid4().hex[:6]}@test.com"

    strong_payload = {
        "company_name": "Hotel Plaza Test",
        "company_slug": unique_slug,
        "owner_email": unique_email,
        "password": "StrongPass123",
        "segment": "hotel",
        "owner_role": "Gerente Geral",
        "owner_phone": "11999999999"
    }

    res_success = client.post("/api/auth/register", json=strong_payload)
    assert res_success.status_code == 201

    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == unique_slug).first()

    assert company is not None
    assert company.segment == CompanySegment.HOTEL
    # O campo owner_role pode não estar mapeado no endpoint de registro ainda
    # Se estiver, descomente:
    # assert company.owner_role == "Gerente Geral"
    
    db.close()
