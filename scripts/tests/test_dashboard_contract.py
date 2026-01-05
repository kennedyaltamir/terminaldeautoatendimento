from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from datetime import datetime
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_dashboard_api_contract():
    """
    Garante que a API do Dashboard retorna a estrutura exata que o Frontend espera.
    Evita quebras silenciosas nos gráficos (Recharts).
    """
    # 1. Setup
    unique_slug = f"dash-contract-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Dashboard Corp",
        slug=unique_slug,
        owner_email=f"dash-{uuid.uuid4().hex[:6]}@test.com"
    )
    db.add(company)
    db.commit()
    
    # Criar um pedido para ter dados
    order = Order(
        company_id=company.id,
        total_amount=100.00,
        status=OrderStatus.DELIVERED,
        payment_status=PaymentStatus.PAID,
        created_at=datetime.now()
    )
    db.add(order)
    db.commit()
    
    # Token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Request
    res = client.get("/api/admin/metrics", headers=headers)
    assert res.status_code == 200
    data = res.json()

    # 3. Validação de Contrato (Tipos e Campos)
    
    # KPI (Agora devem ser números, não strings)
    assert isinstance(data["total_revenue"], (int, float))
    assert isinstance(data["total_orders"], int)
    assert isinstance(data["average_ticket"], (int, float))
    
    # Gráfico de Vendas (AreaChart)
    assert isinstance(data["sales_chart"], list)
    if len(data["sales_chart"]) > 0:
        item = data["sales_chart"][0]
        assert "date" in item
        assert "value" in item
        assert isinstance(item["value"], (int, float))

    # Gráfico de Horas (BarChart)
    assert isinstance(data["sales_by_hour"], list)
    if len(data["sales_by_hour"]) > 0:
        item = data["sales_by_hour"][0]
        assert "hour" in item
        assert "total" in item
        assert isinstance(item["total"], (int, float))

    # Top Produtos (PieChart)
    assert isinstance(data["top_products"], list)
    
    print("✅ Contrato de API do Dashboard validado com sucesso!")