# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:20:00
import sys
import os
from decimal import Decimal
from datetime import datetime
sys.path.append(os.getcwd())
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, PaymentStatus
from sqlalchemy import text

def seed_driver_scenario():
    print("🌱 Semeando cenário de logística...")
    db = SessionLocal()
    try:
        db.execute(text("SET row_security = off"))
        company = db.query(Company).filter(Company.owner_email == "admin@mesaflow.com").first()
        if not company:
            print("❌ Empresa admin não encontrada.")
            return

        # Limpa pedidos antigos para evitar poluição
        db.query(Order).filter(Order.company_id == company.id, Order.status == 'ready').delete()
        
        # Cria pedido fresco
        order = Order(
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.READY,
            payment_status=PaymentStatus.PAID,
            customer_name="CLIENTE TESTE E2E",
            delivery_address="Rua de Teste, 123, Pompéu, MG",
            total_amount=Decimal("45.90"),
            created_at=datetime.now()
        )
        db.add(order)
        db.commit()
        print(f"   ✅ Pedido READY criado para {company.name}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_driver_scenario()
