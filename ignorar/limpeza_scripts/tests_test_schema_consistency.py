import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importação de 'app'
# scripts/tests/test_schema_consistency.py -> sobe 3 níveis -> raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, PaymentProvider
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_company_settings_schema_exposes_payment_provider():
    """
    Valida se o endpoint de configurações retorna o campo 'payment_provider'.
    Isso é crítico para o frontend saber se deve mostrar o botão de desconectar.
    """
    # 1. Setup
    unique_slug = f"schema-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Schema Corp",
        slug=unique_slug,
        owner_email=f"schema-{uuid.uuid4().hex[:6]}@test.com",
        payment_provider=PaymentProvider.MERCADO_PAGO
    )
    db.add(company)
    db.commit()

    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Request
    res = client.get("/api/admin/company/me", headers=headers)
    assert res.status_code == 200
    data = res.json()

    # 3. Validação
    assert "payment_provider" in data
    assert data["payment_provider"] == "MERCADO_PAGO"

    print("✅ Schema de configurações validado com sucesso!")

if __name__ == "__main__":
    test_company_settings_schema_exposes_payment_provider()
