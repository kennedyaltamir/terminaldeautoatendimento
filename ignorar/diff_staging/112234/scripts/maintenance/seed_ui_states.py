# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:20:00
import sys
import os
import uuid
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

# Adiciona a raiz ao path para permitir importações do app
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, OrderType, Table, TableSession, PaymentStatus, Product, Category
from app.core.security import get_password_hash

ADMIN_EMAIL = "admin@mesaflow.com"

def seed_driver_scenario():
    print("🌱 Semeando cenário de logística e estados de UI...")
    db = SessionLocal()
    try:
        # Bypass RLS para o rito de seed administrativo
        db.execute(text("SET row_security = off"))
        
        # 1. Garantir Empresa Admin
        company = db.query(Company).filter(Company.owner_email == ADMIN_EMAIL).first()
        if not company:
            print("   [+] Criando empresa 'hamburgueria-ze'...")
            company = Company(
                name="Hamburgueria do Zé",
                slug="hamburgueria-ze",
                owner_email=ADMIN_EMAIL,
                password_hash=get_password_hash("123456"),
                is_active=True,
                plan_tier="pro"
            )
            db.add(company)
            db.commit()
            db.refresh(company)

        # 2. Garantir Categoria e Produto para testes
        cat = db.query(Category).filter(Category.company_id == company.id).first()
        if not cat:
            cat = Category(company_id=company.id, name="Lanches")
            db.add(cat)
            db.commit()
            db.refresh(cat)
        
        prod = db.query(Product).filter(Product.category_id == cat.id).first()
        if not prod:
            prod = Product(category_id=cat.id, name="X-Bacon Teste", price=Decimal("25.00"), is_available=True)
            db.add(prod)

        # 3. Limpar pedidos 'READY' antigos para evitar poluição visual no teste
        db.query(Order).filter(Order.company_id == company.id, Order.status == 'ready').delete()
        
        # 4. Criar Pedido de Delivery fresco para o motorista
        order = Order(
            id=uuid.uuid4(),
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

        # 5. Garantir Mesa 1 aberta para testes de salão
        table1 = db.query(Table).filter(Table.company_id == company.id, Table.table_number == 1).first()
        if not table1:
            table1 = Table(company_id=company.id, table_number=1, qr_token="token-seguro-mesa-1", is_active=True)
            db.add(table1)
        else:
            table1.qr_token = "token-seguro-mesa-1"
            table1.is_active = True

        db.commit()
        print(f"✨ Cenário populado com sucesso para {company.name}.")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro no seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_driver_scenario()
