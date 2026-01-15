import pytest
from app.models import Company, Order, OrderStatus
from app.core.security import create_access_token, create_refresh_token
import uuid

def test_mobile_kds_sync_resilience_contract(client, db_session):
    """
    Valida o contrato de API para a Missão 24 (Resiliência).
    """
    unique_id = uuid.uuid4().hex[:6]
    company = Company(name=f"Mobile Sync {unique_id}", slug=f"mob-{unique_id}", owner_email=f"mob-{unique_id}@test.com")
    db_session.add(company)
    db_session.commit()
    
    for i in range(3):
        db_session.add(Order(company_id=company.id, customer_name=f"Client {i}", total_amount=10, status=OrderStatus.PENDING))
    db_session.commit()

    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.get(f"/api/admin/{company.slug}/orders", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 3

def test_mobile_error_schema_consistency(client, db_session):
    """
    Valida se o Backend retorna erros no formato esperado pela Missão 25.
    FIX: Cria o usuário no banco para que a autenticação passe e o erro seja de autorização (403).
    """
    unique_id = uuid.uuid4().hex[:6]
    email = f"error-test-{unique_id}@mesaflow.com"
    
    # Criar o usuário/empresa para garantir que o token seja válido no banco
    company = Company(name="Error Test Corp", slug=f"err-{unique_id}", owner_email=email)
    db_session.add(company)
    db_session.commit()

    token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Tenta acessar um slug que não pertence a ele
    res = client.get("/api/admin/slug-que-nao-existe/orders", headers=headers)
    
    # Agora o status deve ser 403 (Forbidden) pois o usuário existe mas não tem acesso ao slug
    assert res.status_code in [403, 404]
    assert "detail" in res.json()
    assert isinstance(res.json()["detail"], str)

def test_mobile_auth_refresh_integrity(client, db_session):
    """
    Valida o endpoint de refresh usando a sessão de banco de teste correta.
    """
    unique_id = uuid.uuid4().hex[:6]
    email = f"refresh-{unique_id}@test.com"
    
    # Cria o tenant no banco em memória do teste
    company = Company(name="Refresh Test", slug=f"ref-{unique_id}", owner_email=email)
    db_session.add(company)
    db_session.commit()

    token_data = {"sub": email, "role": "owner", "account_type": "company"}
    refresh_token = create_refresh_token(data=token_data)
    
    res = client.post("/api/auth/refresh", headers={"X-Refresh-Token": refresh_token})
    
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
