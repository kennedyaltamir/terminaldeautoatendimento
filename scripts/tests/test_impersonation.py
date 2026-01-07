import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, AuditLog, AuditAction
import uuid

client = TestClient(app)

def test_impersonation_security_and_audit():
    """
    Valida o fluxo de God Mode:
    1. Tenta sem segredo (422).
    2. Tenta com segredo errado (401).
    3. Tenta com segredo correto (200).
    4. Verifica se o log de auditoria foi gerado.
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    email = f"victim-{unique_id}@test.com"
    secret = "CHAVE_MESTRA_TESTE_123"
    
    # Define a variável de ambiente para o teste
    os.environ["SUPER_ADMIN_SECRET"] = secret

    db = SessionLocal()
    # Limpa possíveis resíduos
    existing = db.query(Company).filter(Company.owner_email == email).first()
    if existing:
        db.delete(existing)
        db.commit()

    company = Company(
        name="Victim Store",
        slug=f"victim-{unique_id}",
        owner_email=email,
        password_hash="hash"
    )
    db.add(company)
    db.commit()
    company_id = company.id
    db.close()

    # 2. Teste: Sem Header (Deve falhar)
    res_no_header = client.post("/api/auth/impersonate", json={"target_email": email})
    assert res_no_header.status_code == 422 

    # 3. Teste: Segredo Errado
    res_wrong = client.post(
        "/api/auth/impersonate", 
        json={"target_email": email},
        headers={"X-Super-Secret": "ERRADO"}
    )
    assert res_wrong.status_code == 401

    # 4. Teste: Sucesso
    res_ok = client.post(
        "/api/auth/impersonate", 
        json={"target_email": email},
        headers={"X-Super-Secret": secret}
    )
    assert res_ok.status_code == 200
    data = res_ok.json()
    assert "access_token" in data
    assert data["company_slug"] == f"victim-{unique_id}"

    # 5. Verificar Auditoria
    db = SessionLocal()
    log = db.query(AuditLog).filter(
        AuditLog.company_id == company_id,
        AuditLog.action == AuditAction.IMPERSONATE
    ).first()

    assert log is not None
    assert log.details["target"] == email
    db.close()

    print("\n✅ Teste de Impersonation (God Mode) passou com sucesso!")

if __name__ == "__main__":
    test_impersonation_security_and_audit()
