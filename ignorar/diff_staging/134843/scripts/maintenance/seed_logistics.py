# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:55:00
import sys
import os
import uuid
import json
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy import text

# Adiciona a raiz ao path
sys.path.append(os.getcwd())
from app.database import SessionLocal
from app.models import Company, Employee, Order, OrderItem, Product, Category, DriverLedger
from app.core.security import get_password_hash
from app.models.core import OrderStatus, PaymentStatus, OrderType, UserRole, PaymentMethod, LedgerType

def log(msg):
    print(f"[SEED_LOGISTICS] {msg}")

def seed():
    db = SessionLocal()
    # Timestamp fixo para garantir que o pedido de teste apareça no topo (mais recente)
    NOW = datetime.now() 
    
    try:
        log("🧹 Limpando dados de logística...")
        db.execute(text("DELETE FROM driver_ledger"))
        db.execute(text("DELETE FROM order_feedbacks WHERE order_id IN (SELECT id FROM orders WHERE order_type = 'delivery')"))
        db.execute(text("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE order_type = 'delivery')"))
        db.execute(text("DELETE FROM orders WHERE order_type = 'delivery'"))
        db.commit()

        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        if not company:
            log("❌ Empresa não encontrada.")
            return

        # Garante produto para o pedido
        product = db.query(Product).first()
        if not product:
            log("❌ Nenhum produto no banco para criar pedido.")
            return

        log("📦 Criando massa de dados determinística...")

        # Pedido 1: O ALVO PRINCIPAL (Mais recente)
        order_target = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.READY,
            payment_status=PaymentStatus.PAID,
            payment_method=PaymentMethod.ONLINE,
            customer_name="Cliente Happy Path",
            delivery_address="Rua Principal, 100",
            total_amount=Decimal("50.00"),
            created_at=NOW
        )
        db.add(order_target)
        db.add(OrderItem(order_id=order_target.id, product_id=product.id, quantity=1, unit_price=product.price))

        # Pedido 2: O FALLBACK (Mais antigo)
        order_fallback = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.READY,
            payment_status=PaymentStatus.PENDING,
            payment_method=PaymentMethod.CASH,
            customer_name="Cliente Dinheiro",
            delivery_address="Rua Secundária, 200",
            total_amount=Decimal("35.00"),
            created_at=NOW - timedelta(minutes=10)
        )
        db.add(order_fallback)
        db.add(OrderItem(order_id=order_fallback.id, product_id=product.id, quantity=1, unit_price=product.price))

        db.commit()
        log("✅ Seed de logística estabilizado.")
        
    except Exception as e:
        db.rollback()
        log(f"❌ Erro: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
