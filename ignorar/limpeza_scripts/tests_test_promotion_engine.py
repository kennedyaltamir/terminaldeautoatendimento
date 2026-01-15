from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Promotion, DiscountType
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

client = TestClient(app)

def test_promotion_logic():
    """
    Testa o motor de promoções:
    1. Criação de Cupom (Percentual).
    2. Validação de Cupom Válido.
    3. Validação de Cupom Expirado.
    4. Validação de Valor Mínimo.
    """
    # 1. Setup
    unique_slug = f"promo-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Promo Corp",
        slug=unique_slug,
        owner_email=f"promo-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()

    # Cupom 10% OFF (Válido)
    promo_valid = Promotion(
        company_id=company.id,
        name="Bem Vindo",
        code="BEMVINDO10",
        discount_type=DiscountType.PERCENTAGE,
        discount_value=Decimal("10.00"),
        min_order_value=Decimal("50.00"),
        is_active=True
    )
    
    # Cupom Expirado
    promo_expired = Promotion(
        company_id=company.id,
        name="Natal Passado",
        code="NATAL25",
        discount_type=DiscountType.FIXED,
        discount_value=Decimal("20.00"),
        end_date=datetime.now() - timedelta(days=1),
        is_active=True
    )

    db.add_all([promo_valid, promo_expired])
    db.commit()
    
    company_id = company.id
    db.close()

    # 2. Teste: Cupom Válido
    payload_valid = {
        "code": "BEMVINDO10",
        "total_amount": 100.00
    }
    res_valid = client.post(f"/api/{unique_slug}/cart/validate-coupon", json=payload_valid)
    assert res_valid.status_code == 200
    data = res_valid.json()
    assert data["valid"] is True
    assert float(data["discount_amount"]) == 10.00 # 10% de 100
    assert float(data["final_total"]) == 90.00

    # 3. Teste: Valor Mínimo não atingido
    payload_min = {
        "code": "BEMVINDO10",
        "total_amount": 40.00 # Mínimo é 50
    }
    res_min = client.post(f"/api/{unique_slug}/cart/validate-coupon", json=payload_min)
    assert res_min.json()["valid"] is False
    assert "Valor mínimo" in res_min.json()["message"]

    # 4. Teste: Cupom Expirado
    payload_exp = {
        "code": "NATAL25",
        "total_amount": 100.00
    }
    res_exp = client.post(f"/api/{unique_slug}/cart/validate-coupon", json=payload_exp)
    assert res_exp.json()["valid"] is False
    assert "expirado" in res_exp.json()["message"]

    # 5. Teste: Cupom Inexistente
    payload_404 = {
        "code": "NAOEXISTE",
        "total_amount": 100.00
    }
    res_404 = client.post(f"/api/{unique_slug}/cart/validate-coupon", json=payload_404)
    assert res_404.json()["valid"] is False