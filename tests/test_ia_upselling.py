from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Product, Category, Order, OrderItem, OrderStatus
from app.services.recommendation_service import RecommendationService
from decimal import Decimal
import uuid

client = TestClient(app)

def test_recommendation_engine_logic():
    """
    Testa se o motor de IA identifica corretamente padrões de compra.
    Cenário:
    - 3 Pedidos contêm (Burger + Refri).
    - 1 Pedido contém (Burger + Batata).
    - Resultado Esperado: Burger deve recomendar Refri (Alta confiança) e talvez Batata.
    """
    
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    db = SessionLocal()
    
    company = Company(name=f"IA Corp {unique_id}", slug=f"ia-{unique_id}", owner_email=f"ia-{unique_id}@test.com")
    db.add(company)
    db.commit()
    
    cat = Category(company_id=company.id, name="Geral")
    db.add(cat)
    db.commit()
    
    p_burger = Product(category_id=cat.id, name="Burger", price=20)
    p_refri = Product(category_id=cat.id, name="Refri", price=5)
    p_batata = Product(category_id=cat.id, name="Batata", price=10)
    db.add_all([p_burger, p_refri, p_batata])
    db.commit()
    
    # IDs
    burger_id = p_burger.id
    refri_id = p_refri.id
    batata_id = p_batata.id
    company_id = str(company.id)
    
    # 2. Gerar Histórico de Vendas
    # 3x Burger + Refri
    for _ in range(3):
        order = Order(company_id=company.id, total_amount=25, status=OrderStatus.DELIVERED)
        db.add(order)
        db.commit()
        db.add(OrderItem(order_id=order.id, product_id=burger_id, quantity=1, unit_price=20))
        db.add(OrderItem(order_id=order.id, product_id=refri_id, quantity=1, unit_price=5))
        db.commit()
        
    # 1x Burger + Batata
    order = Order(company_id=company.id, total_amount=30, status=OrderStatus.DELIVERED)
    db.add(order)
    db.commit()
    db.add(OrderItem(order_id=order.id, product_id=burger_id, quantity=1, unit_price=20))
    db.add(OrderItem(order_id=order.id, product_id=batata_id, quantity=1, unit_price=10))
    db.commit()
    
    # 3. Rodar Motor de IA (Síncrono para teste)
    count = RecommendationService.generate_recommendations(db, company_id, min_confidence=0.5)
    
    # 4. Verificar Resultados
    # Burger apareceu 4 vezes.
    # Refri apareceu 3 vezes com Burger -> Confiança 3/4 = 0.75 (Deve recomendar)
    # Batata apareceu 1 vez com Burger -> Confiança 1/4 = 0.25 (Abaixo de 0.5, não deve recomendar)
    
    db.refresh(p_burger)
    recommendations = p_burger.recommendations
    rec_ids = [p.id for p in recommendations]
    
    assert refri_id in rec_ids, "Burger deveria recomendar Refri (75% confiança)"
    assert batata_id not in rec_ids, "Burger NÃO deveria recomendar Batata (25% confiança < 50% threshold)"
    
    db.close()