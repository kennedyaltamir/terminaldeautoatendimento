# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 10:20:00
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Category, Product, AuditLog, AuditAction
from app.core.security import create_access_token
from decimal import Decimal
import uuid

client = TestClient(app)

def test_audit_log_lifecycle():
    """
    Teste unificado de Auditoria:
    1. Cria Empresa e Produto.
    2. Atualiza Produto (Gera Log).
    3. Verifica Log no Banco.
    4. Verifica Log via API (Endpoint).
    """
    # --- SETUP ---
    unique_slug = f"audit-life-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Audit Lifecycle Corp",
        slug=unique_slug,
        owner_email=f"audit-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()

    category = Category(company_id=company.id, name="Geral")
    db.add(category)
    db.commit()

    product = Product(
        category_id=category.id,
        name="Produto Auditado",
        price=Decimal("10.00")
    )
    db.add(product)
    db.commit()

    product_id = product.id
    company_id = company.id

    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company", "company_id": str(company.id)})
    headers = {"Authorization": f"Bearer {token}"}

    db.close()

    # --- AÇÃO: Atualizar Produto ---
    # O payload agora deve ser em centavos (2000 = R$ 20,00)
    payload = {"price": 2000}
    res_update = client.patch(f"/api/admin/menu/products/{product_id}", headers=headers, json=payload)
    assert res_update.status_code == 200

    # --- VERIFICAÇÃO 1: Banco de Dados ---
    db = SessionLocal()
    log_db = db.query(AuditLog).filter(
        AuditLog.company_id == company_id,
        AuditLog.resource == "Product",
        AuditLog.resource_id == str(product_id),
        AuditLog.action == AuditAction.UPDATE
    ).first()

    assert log_db is not None
    # O log armazena o valor decimal do banco, não centavos
    assert float(log_db.details["old"]["price"]) == 10.0
    assert float(log_db.details["new"]["price"]) == 20.0
    db.close()

    # --- VERIFICAÇÃO 2: API Endpoint ---
    res_api = client.get("/api/admin/audit", headers=headers)
    assert res_api.status_code == 200
    logs = res_api.json()

    my_log = next((l for l in logs if l["resource_id"] == str(product_id)), None)

    assert my_log is not None
    assert my_log["action"] == "update"
    assert my_log["user_role"] == "owner"
