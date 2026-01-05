from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus, FiscalStatus
from app.core.security import create_access_token
from decimal import Decimal
import uuid
import time

client = TestClient(app)

def test_fiscal_background_processing():
    """
    Testa se a emissão fiscal ocorre em background e atualiza o status.
    Usa o MockProvider (padrão).
    """
    # 1. Setup
    unique_slug = f"fiscal-arch-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Fiscal Arch Corp",
        slug=unique_slug,
        owner_email=f"fiscal-arch-{uuid.uuid4().hex[:6]}@test.com",
        cnpj="12345678000199"
    )
    db.add(company)
    db.commit()
    
    order = Order(
        company_id=company.id,
        total_amount=Decimal("100.00"),
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        customer_name="Fiscal Client"
    )
    db.add(order)
    db.commit()
    
    order_id = str(order.id)
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    db.close()

    # 2. Solicitar Emissão (Deve retornar 200 Processing)
    res = client.post(f"/api/admin/fiscal/orders/{order_id}/emit", headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "processing"

    # 3. Aguardar Background Task (Mock tem sleep de 1s)
    time.sleep(2)

    # 4. Verificar se atualizou para EMITTED
    db = SessionLocal()
    updated_order = db.query(Order).filter(Order.id == order_id).first()
    
    assert updated_order.fiscal_status == FiscalStatus.EMITTED
    assert updated_order.nfe_key is not None
    assert "mock_ref" in updated_order.fiscal_reference_id
    db.close()

def test_factory_switching():
    """
    Testa se a Factory respeita a variável de ambiente.
    """
    from app.services.fiscal.factory import get_fiscal_provider
    from app.services.fiscal.providers.focus_nfe import FocusNFeProvider
    from app.services.fiscal.providers.mock import MockProvider
    
    # Default -> Mock
    with patch.dict("os.environ", {}, clear=True):
        assert isinstance(get_fiscal_provider(), MockProvider)
        
    # Configured -> Focus
    with patch.dict("os.environ", {"FISCAL_PROVIDER": "focus"}):
        assert isinstance(get_fiscal_provider(), FocusNFeProvider)