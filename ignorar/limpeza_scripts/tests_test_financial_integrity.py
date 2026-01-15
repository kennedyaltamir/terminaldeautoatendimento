from fastapi.testclient import TestClient
from app.main import app
from app.services.payment_service import PaymentService
from decimal import Decimal
import uuid

client = TestClient(app)

def test_split_calculation_precision():
    service = PaymentService()
    fee = service.calculate_split(Decimal("100.00"), Decimal("1.5"))
    assert fee == Decimal("1.50")

def test_admin_can_update_payment_settings():
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Payload Inválido
    bad_payload = {"mp_access_token": "TOKEN_INVALIDO_123"}
    res_bad = client.patch("/api/admin/company/me", headers=headers, json=bad_payload)
    assert res_bad.status_code == 400
    # Mensagem atualizada conforme implementação
    assert "inválido" in res_bad.json()["detail"].lower()

    # 3. Payload Válido
    valid_token = "APP_USR-1234567890-TEST-TOKEN"
    good_payload = {"mp_access_token": valid_token}
    res_good = client.patch("/api/admin/company/me", headers=headers, json=good_payload)
    assert res_good.status_code == 200
    # O retorno é mascarado
    assert "****" in res_good.json()["mp_access_token"]
