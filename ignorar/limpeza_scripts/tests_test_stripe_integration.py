from unittest.mock import patch
from app.models import Company, PlanTier
import uuid

def test_stripe_webhook_checkout_completed(client, db_session):
    unique_slug = f"stripe-int-{uuid.uuid4().hex[:6]}"
    company = Company(
        name="Stripe Int Corp",
        slug=unique_slug,
        owner_email=f"stripe-{unique_slug}@test.com",
        plan_tier=PlanTier.FREE
    )
    db_session.add(company)
    db_session.commit()
    company_id = str(company.id)

    mock_event = {
        "id": "evt_test",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "metadata": {"company_id": company_id},
                "subscription": "sub_test_123"
            }
        }
    }

    with patch("app.services.stripe_service.StripeService.construct_event", return_value=mock_event):
        response = client.post(
            "/api/webhooks/stripe",
            json=mock_event,
            headers={"stripe-signature": "valid_mock_sig"}
        )
        assert response.status_code == 200

        db_session.refresh(company)
        assert company.plan_tier == PlanTier.PRO

def test_stripe_webhook_subscription_deleted(client, db_session):
    unique_slug = f"stripe-del-{uuid.uuid4().hex[:6]}"
    company = Company(
        name="Stripe Del Corp",
        slug=unique_slug,
        owner_email=f"del-{unique_slug}@test.com",
        plan_tier=PlanTier.PRO,
        stripe_subscription_id="sub_to_cancel",
        subscription_status="active"
    )
    db_session.add(company)
    db_session.commit()

    mock_event = {
        "id": "evt_test_del",
        "object": "event",
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_to_cancel",
                "status": "canceled"
            }
        }
    }

    with patch("app.services.stripe_service.StripeService.construct_event", return_value=mock_event):
        client.post("/api/webhooks/stripe", json=mock_event, headers={"stripe-signature": "valid"})

        db_session.refresh(company)
        assert company.plan_tier == PlanTier.FREE
