from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company
from app.core.security import create_access_token
import uuid
import pytest

client = TestClient(app)

def test_feature_flags_api_contract_and_impersonation_security():
    """
    PoC: Valida contrato de API e barreira de segurança de Impersonation.
    """
    db = SessionLocal()
    
    try:
        # 1. Setup: Criar empresa de teste isolada
        uid = uuid.uuid4()
        email = f"admin-{uid.hex[:6]}@mesaflow.com"
        company = Company(
            id=uid, 
            name="Contract Test Corp", 
            slug=f"test-{uid.hex[:6]}", 
            owner_email=email
        )
        db.add(company)
        db.commit()

        # 2. Geração de Tokens (Normal vs Impersonator)
        # O backend espera a claim 'impersonator' no payload do JWT
        token_normal = create_access_token(data={
            "sub": email, 
            "role": "owner", 
            "account_type": "company", 
            "impersonator": False
        })
        
        token_support = create_access_token(data={
            "sub": email, 
            "role": "owner", 
            "account_type": "company", 
            "impersonator": True
        })

        # 3. Validação do Contrato GET (Listagem)
        # Deve retornar um dicionário { key: bool }
        res_get = client.get(
            "/api/admin/features", 
            headers={"Authorization": f"Bearer {token_normal}"}
        )
        assert res_get.status_code == 200
        data = res_get.json()
        assert isinstance(data, dict), "O retorno do GET deve ser um objeto JSON (dict)"
        for key, value in data.items():
            assert isinstance(value, bool), f"A flag {key} deve ser booleana"

        # 4. Validação de Segurança POST (Bloqueio de Usuário Comum)
        # Mesmo sendo o 'owner' da empresa, não pode alterar flags sem estar em modo suporte
        res_post_fail = client.post(
            "/api/admin/features",
            headers={"Authorization": f"Bearer {token_normal}"},
            json={"key": "poc_beta_feature", "is_enabled": True}
        )
        assert res_post_fail.status_code == 403, "Usuário comum não deve ter permissão de escrita em flags"
        assert "suporte" in res_post_fail.json()["detail"].lower()

        # 5. Validação de Segurança POST (Permissão de Impersonator)
        res_post_success = client.post(
            "/api/admin/features",
            headers={"Authorization": f"Bearer {token_support}"},
            json={"key": "poc_beta_feature", "is_enabled": True}
        )
        assert res_post_success.status_code == 200, "Impersonator deve conseguir alterar flags"
        assert res_post_success.json()["status"] is True

        # 6. Validação de Integridade e Cache
        # O GET subsequente deve refletir a alteração imediatamente
        res_get_final = client.get(
            "/api/admin/features", 
            headers={"Authorization": f"Bearer {token_normal}"}
        )
        assert res_get_final.json().get("poc_beta_feature") is True, "A alteração não foi persistida ou o cache não invalidou"

        print("\n✅ PoC de Feature Flags concluída: Contrato e Segurança validados.")

    finally:
        db.close()

if __name__ == "__main__":
    # Execução direta para debug rápido
    test_feature_flags_api_contract_and_impersonation_security()
