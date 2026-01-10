from app.models import Company, Product, Category
from decimal import Decimal
import uuid

def test_create_order_with_payment_method(client, db_session):
    """Valida se o pedido salva corretamente a forma de pagamento escolhida"""
    # Setup
    unique_slug = f"pay-method-{uuid.uuid4().hex[:6]}"
    company = Company(name="Pay Method Corp", slug=unique_slug, owner_email=f"pm-{unique_slug}@test.com")
    db_session.add(company)
    db_session.commit()

    cat = Category(company_id=company.id, name="Geral")
    db_session.add(cat)
    db_session.commit()
    
    prod = Product(category_id=cat.id, name="Item", price=Decimal("10.00"))
    db_session.add(prod)
    db_session.commit()

    payload = {
        "table_id": None,
        "qr_token": "staff-override",
        "order_type": "takeout",
        "customer_name": "Cliente Pagador",
        "payment_method": "pix",
        "items": [{"product_id": prod.id, "quantity": 1}]
    }
    response = client.post(f"/api/{unique_slug}/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["payment_method"] == "pix"
    assert data["payment_status"] == "pending"
