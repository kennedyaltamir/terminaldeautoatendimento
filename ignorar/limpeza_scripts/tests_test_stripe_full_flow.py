from unittest.mock import patch
from app.models import Company, PlanTier
import uuid

def test_full_subscription_lifecycle(client, db_session):
    """
    Testa o ciclo completo de vida da assinatura.
    """
    unique_slug = f"saas-test-{uuid.uuid4().hex[:6]}"
    company = Company(
        name="SaaS Cycle Corp",
        slug=unique_slug,
        owner_email=f"ceo-{unique_slug}@test.com",
        plan_tier=PlanTier.FREE
    )
    db_session.add(company)
    db_session.commit()
    company_id = str(company.id)

    # Mock do evento
    mock_event = {
        "id": "evt_test_webhook",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {"company_id": company_id},
                "subscription": "sub_active_123"
            }
        }
    }

    # Patch no construct_event para ignorar assinatura real
    with patch("app.services.stripe_service.StripeService.construct_event", return_value=mock_event):
        # O endpoint espera um body raw bytes, o TestClient json=... serializa.
        # O header stripe-signature é obrigatório para passar na validação inicial do endpoint
        res = client.post(
            "/api/webhooks/stripe", 
            json=mock_event, 
            headers={"stripe-signature": "dummy_sig"}
        )
        
        # Se der 400, imprime o erro para debug
        if res.status_code != 200:
            print(f"Erro Webhook: {res.json()}")
            
        assert res.status_code == 200

    db_session.refresh(company)
    assert company.plan_tier == PlanTier.PRO
