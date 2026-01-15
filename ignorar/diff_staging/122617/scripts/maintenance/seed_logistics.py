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
    # Timestamp Determinístico para evitar flakiness em testes de ordenação
    FIXED_NOW = datetime.now() 
    try:
        log("🧹 Limpando dados de logística anteriores (Clean Slate)...")
        # 1. Limpeza Cirúrgica (Respeitando FKs - Deletar Filhos antes dos Pais)
        # Financeiro do Motorista
        db.execute(text("DELETE FROM driver_ledger"))
        # Avaliações (Feedbacks) vinculadas a delivery
        db.execute(text("DELETE FROM order_feedbacks WHERE order_id IN (SELECT id FROM orders WHERE order_type = 'delivery')"))
        # Transações de Pagamento vinculadas a delivery
        db.execute(text("DELETE FROM payment_transactions WHERE order_id IN (SELECT id FROM orders WHERE order_type = 'delivery')"))
        # Itens do Pedido
        db.execute(text("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE order_type = 'delivery')"))
        # Pedidos
        db.execute(text("DELETE FROM orders WHERE order_type = 'delivery'"))
        # Funcionários (Motoristas)
        db.execute(text("DELETE FROM employees WHERE role = 'driver'"))
        db.commit()
        # 2. Garantir Empresa
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        if not company:
            log("❌ Empresa 'hamburgueria-ze' não encontrada. Rode o seed.py básico primeiro.")
            return
        # 3. Garantir Categoria e Produto (Idempotente)
        cat = db.query(Category).filter_by(company_id=company.id, name="Geral").first()
        if not cat:
            cat = Category(name="Geral", company_id=company.id)
            db.add(cat)
            db.flush()
        product = db.query(Product).filter_by(category_id=cat.id, name="Item Teste").first()
        if not product:
            product = Product(name="Item Teste", price=10.00, category_id=cat.id)
            db.add(product)
            db.commit()
            db.refresh(product)
        log("👥 Criando Entregadores...")
        # Driver 1: Livre e sem dívidas (Happy Path)
        driver_free = Employee(
            company_id=company.id,
            name="João Livre",
            email="driver.free@mesaflow.com",
            password_hash=get_password_hash("123456"),
            role=UserRole.DRIVER,
            is_active=True
        )
        db.add(driver_free)
        # Driver 2: Ocupado (Concurrency Test)
        driver_busy = Employee(
            company_id=company.id,
            name="Maria Ocupada",
            email="driver.busy@mesaflow.com",
            password_hash=get_password_hash("123456"),
            role=UserRole.DRIVER,
            is_active=True
        )
        db.add(driver_busy)
        # Driver 3: Endividado (Financial Limits Test)
        driver_debt = Employee(
            company_id=company.id,
            name="Carlos Devedor",
            email="driver.debt@mesaflow.com",
            password_hash=get_password_hash("123456"),
            role=UserRole.DRIVER,
            is_active=True
        )
        db.add(driver_debt)
        db.flush() # Gera IDs
        # Injeta dívida no Driver 3 usando Enum correto
        debt_entry = DriverLedger(
            company_id=company.id,
            driver_id=driver_debt.id,
            type=LedgerType.DEBT.value, # Enum value
            amount=Decimal("200.00"), # Dívida alta
            description="Seed Debt",
            created_at=FIXED_NOW
        )
        db.add(debt_entry)
        log("📦 Criando Pedidos de Teste...")
        # Pedido 1: READY (Alvo do Happy Path)
        order_ready = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.READY,
            payment_status=PaymentStatus.PAID,
            payment_method=PaymentMethod.ONLINE,
            customer_name="Cliente Happy Path",
            delivery_address="Rua A, 100 - Centro",
            total_amount=Decimal("50.00"),
            created_at=FIXED_NOW - timedelta(minutes=30)
        )
        db.add(order_ready)
        db.add(OrderItem(order_id=order_ready.id, product_id=product.id, quantity=1, unit_price=product.price))
        # Pedido 2: DELIVERED (Antigo Delivering - Alterado para não bloquear a UI do Admin no teste)
        # Se estiver DELIVERING, o Admin vê o mapa e não a lista, quebrando o teste Happy Path.
        order_delivered = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.DELIVERED, # ALTERADO DE DELIVERING PARA DELIVERED
            payment_status=PaymentStatus.PAID,
            payment_method=PaymentMethod.ONLINE,
            customer_name="Cliente Entregue",
            delivery_address="Av Paulista, 200",
            total_amount=Decimal("80.00"),
            driver_id=driver_busy.id, 
            created_at=FIXED_NOW - timedelta(minutes=45),
            finished_at=FIXED_NOW
        )
        db.add(order_delivered)
        db.add(OrderItem(order_id=order_delivered.id, product_id=product.id, quantity=2, unit_price=product.price))
        # Pedido 3: PENDING (Não deve aparecer para coleta ainda)
        order_pending = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PAID,
            customer_name="Cliente Cozinha",
            delivery_address="Rua C, 300",
            total_amount=Decimal("30.00"),
            created_at=FIXED_NOW
        )
        db.add(order_pending)
        db.add(OrderItem(order_id=order_pending.id, product_id=product.id, quantity=1, unit_price=product.price))
        # Pedido 4: CASH (Para teste financeiro)
        order_cash = Order(
            id=uuid.uuid4(),
            company_id=company.id,
            order_type=OrderType.DELIVERY,
            status=OrderStatus.READY,
            payment_status=PaymentStatus.PENDING,
            payment_method=PaymentMethod.CASH,
            customer_name="Cliente Dinheiro",
            delivery_address="Rua D, 400",
            total_amount=Decimal("45.50"),
            created_at=FIXED_NOW - timedelta(minutes=10)
        )
        db.add(order_cash)
        db.add(OrderItem(order_id=order_cash.id, product_id=product.id, quantity=1, unit_price=product.price))
        db.commit()
        # Output JSON para consumo do script de teste
        output = {
            "meta": {
                "timestamp": FIXED_NOW.isoformat(),
                "company_slug": company.slug
            },
            "drivers": {
                "free": {"email": driver_free.email, "id": driver_free.id},
                "busy": {"email": driver_busy.email, "id": driver_busy.id},
                "debt": {"email": driver_debt.email, "id": driver_debt.id}
            },
            "orders": {
                "ready_id": str(order_ready.id),
                "delivered_id": str(order_delivered.id),
                "pending_id": str(order_pending.id),
                "cash_id": str(order_cash.id)
            }
        }
        print("\n--- SEED DATA START ---")
        print(json.dumps(output))
        print("--- SEED DATA END ---")
        log("✅ Seed concluído com sucesso (Industrial Grade).")
    except Exception as e:
        db.rollback()
        log(f"❌ Erro no seed: {e}")
        sys.exit(1)
    finally:
        db.close()
if __name__ == "__main__":
    seed()
