from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.database import SessionLocal
from app.models import Company, PlanTier
import pytest

client = TestClient(app)

def test_billing_routes_protection():
    """Garante que apenas donos acessam rotas de cobrança"""
    response = client.post("/api/admin/billing/upgrade")
    assert response.status_code == 401

def test_stripe_webhook_signature_validation():
    """Garante que o webhook rejeita chamadas sem assinatura válida"""
    response = client.post(
        "/api/webhooks/stripe",
        content=b'{"id": "evt_test"}',
        headers={"stripe-signature": "invalid"}
    )
    assert response.status_code == 400

def test_upgrade_flow_logic():
    """Valida se o endpoint de upgrade retorna uma URL simulada"""
    # 1. Login
    login_res = client.post("/api/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Simular a chamada ao Stripe para não depender de chaves reais no teste
    with patch("app.services.stripe_service.StripeService.create_checkout_session") as mock_stripe:
        mock_stripe.return_value = "https://checkout.stripe.com/pay/test_session"
        
        response = client.post("/api/admin/billing/upgrade", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["url"] == "https://checkout.stripe.com/pay/test_session"
        mock_stripe.assert_called_once()