# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:45:00
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
        # 🛡️ BYPASS RLS PARA SETUP (Como Superuser)
        db.execute(text("SET row_security = off"))
        
        print("🧹 Limpando dados de logística (Ordem Segura)...")
        # 1. Deleta itens primeiro para evitar ForeignKeyViolation
        db.execute(text("""
            DELETE FROM order_items 
            WHERE order_id IN (SELECT id FROM orders WHERE order_type = 'delivery')
        """))
        
        # 2. Deleta os pedidos
        db.execute(text("DELETE FROM orders WHERE order_type = 'delivery'"))
        db.commit()

        # Busca empresa e produto existentes
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        product = db.query(Product).first()

        if not company or not product:
            print("❌ Erro: Empresa ou Produto não encontrados. Rode o seed.py base primeiro.")
            return

        print("📦 Criando massa de dados determinística...")
        
        # Pedido de Teste
        order_id = uuid.uuid4()
        new_order = Order(
            id=order_id,
            company_id=company.id,
            order_type="delivery",
            status="ready",
            payment_status="paid",
            customer_name="Cliente Happy Path",
            delivery_address="Rua Principal, 100, Pompéu, MG",
            total_amount=Decimal("50.00"),
            created_at=datetime.now()
        )
        db.add(new_order)
        
        # Item do Pedido
        db.add(OrderItem(
            order_id=order_id, 
            product_id=product.id, 
            quantity=1, 
            unit_price=product.price
        ))

        db.commit()
        print("✅ Seed de logística concluído com sucesso.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro crítico no seed: {e}")
        sys.exit(1)
    finally:
        # Garante que o RLS seja reativado mesmo em caso de erro
        try:
            db.execute(text("SET row_security = on"))
        except:
            pass
        db.close()

if __name__ == "__main__":
    seed()

