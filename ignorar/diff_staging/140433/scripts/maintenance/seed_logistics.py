# DOMAIN: DEVOPS_SCRIPTS
import sys
import os
import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy import text

# Adiciona a raiz ao path
sys.path.append(os.getcwd())
from app.database import SessionLocal
from app.models import Company, Order, OrderItem, Product

def seed():
    db = SessionLocal()
    try:
        # 🛡️ BYPASS RLS PARA SETUP
        db.execute(text("SET row_security = off"))
        
        print("🧹 Limpando dados de logística...")
        db.execute(text("DELETE FROM orders WHERE order_type = 'delivery'"))
        db.commit()

        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        product = db.query(Product).first()

        print("📦 Criando pedidos de teste...")
        
        # Pedido 1: Happy Path
        order1 = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type="delivery",
            status="ready",
            payment_status="paid",
            customer_name="Cliente Happy Path",
            delivery_address="Rua Principal, 100",
            total_amount=Decimal("50.00"),
            created_at=datetime.now()
        )
        db.add(order1)
        db.add(OrderItem(order_id=order1.id, product_id=product.id, quantity=1, unit_price=product.price))

        # Pedido 2: Fallback
        order2 = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type="delivery",
            status="ready",
            payment_status="pending",
            customer_name="Cliente Dinheiro",
            delivery_address="Rua Secundária, 200",
            total_amount=Decimal("35.00"),
            created_at=datetime.now() - timedelta(minutes=5)
        )
        db.add(order2)
        db.add(OrderItem(order_id=order2.id, product_id=product.id, quantity=1, unit_price=product.price))

        db.commit()
        print("✅ Seed concluído.")
    finally:
        db.execute(text("SET row_security = on"))
        db.close()

if __name__ == "__main__":
    seed()
