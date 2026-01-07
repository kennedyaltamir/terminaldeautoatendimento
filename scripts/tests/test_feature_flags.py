from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, FeatureFlag
from app.core.security import create_access_token
import uuid
import pytest

client = TestClient(app)

def test_feature_flag_security_enforcement():
    """
    Valida se o sistema bloqueia alterações de flags por usuários comuns
    e permite apenas para usuários com a claim 'impersonator'.
    """
    db = SessionLocal()
    
    try:
        # 1. Setup de Empresa
        unique_id = uuid.uuid4()
        email = f"owner-{unique_id.hex[:6]}@test.com"
        company = Company(
            id=unique_id,
            name="Security Test Corp",
            slug=f"sec-{unique_id.hex[:6]}",
            owner_email=email
        )
        db.add(company)
        db.commit()

        # 2. Token de Dono Comum (Sem Impersonation)
        token_normal = create_access_token(data={
            "sub": email, 
            "role": "owner", 
            "account_type": "company",
            "impersonator": False
        })

        # 3. Token de Suporte (Com Impersonation)
        token_support = create_access_token(data={
            "sub": email, 
            "role": "owner", 
            "account_type": "company",
            "impersonator": True
        })

        # 4. Tentar alterar flag como usuário normal (Deve falhar 403)
        res_fail = client.post(
            "/api/admin/features",
            headers={"Authorization": f"Bearer {token_normal}"},
            json={"key": "beta_feature_x", "is_enabled": True}
        )
        assert res_fail.status_code == 403
        assert "suporte" in res_fail.json()["detail"].lower()

        # 5. Alterar flag como suporte (Deve passar 200)
        res_success = client.post(
            "/api/admin/features",
            headers={"Authorization": f"Bearer {token_support}"},
            json={"key": "beta_feature_x", "is_enabled": True}
        )
        assert res_success.status_code == 200
        assert res_success.json()["status"] is True

        # 6. Verificar se a flag foi persistida
        res_get = client.get(
            "/api/admin/features",
            headers={"Authorization": f"Bearer {token_normal}"}
        )
        assert res_get.status_code == 200
        assert res_get.json().get("beta_feature_x") is True

    finally:
        db.close()

if __name__ == "__main__":
    test_feature_flag_security_enforcement()
