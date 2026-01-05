from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.database import SessionLocal
from app.models import Company, PlanTier
import pytest

client = TestClient(app)

def test_stripe_webhook_checkout_completed():
    """Simula o sucesso de um pagamento no Stripe e ativação do plano PRO"""
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    company_id = str(company.id)
    db.close()

    # Mock do evento do Stripe
    mock_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {"company_id": company_id},
                "subscription": "sub_test_123"
            }
        }
    }

    with patch("app.services.stripe_service.StripeService.handle_webhook", return_value=mock_event):
        response = client.post(
            "/api/webhooks/stripe",
            json=mock_event,
            headers={"stripe-signature": "valid_mock_sig"}
        )
        assert response.status_code == 200
        
        # Verificar se a empresa agora é PRO
        db = SessionLocal()
        updated_company = db.query(Company).filter(Company.id == company_id).first()
        assert updated_company.plan_tier == PlanTier.PRO
        assert updated_company.stripe_subscription_id == "sub_test_123"
        db.close()

def test_stripe_webhook_subscription_deleted():
    """Simula o cancelamento de uma assinatura e retorno ao plano FREE"""
    db = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    company.stripe_subscription_id = "sub_to_cancel"
    company.plan_tier = PlanTier.PRO
    db.commit()
    db.close()

    mock_event = {
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_to_cancel",
                "status": "canceled"
            }
        }
    }

    with patch("app.services.stripe_service.StripeService.handle_webhook", return_value=mock_event):
        client.post("/api/webhooks/stripe", json=mock_event, headers={"stripe-signature": "valid"})
        
        db = SessionLocal()
        updated_company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        assert updated_company.plan_tier == PlanTier.FREE
        assert updated_company.subscription_status == "canceled"
        db.close()