
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 00:40:00
import sys
import os
sys.path.append(os.getcwd())

from app.database import SessionLocal, engine
from app.models import Base, Company, Category, Product, Table
from app.core.security import get_password_hash
from decimal import Decimal
import uuid

def seed():
    print("🌱 Iniciando Seed de Produção...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Criar Empresa Principal
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    if not company:
        company = Company(
            name="Hamburgueria do Zé",
            slug="hamburgueria-ze",
            owner_email="admin@mesaflow.com",
            password_hash=get_password_hash("123456"),
            is_active=True,
            plan_tier="pro"
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        print("   ✅ Empresa 'hamburgueria-ze' criada.")

    # 2. Criar Categoria
    cat = db.query(Category).filter(Category.company_id == company.id).first()
    if not cat:
        cat = Category(name="Lanches", company_id=company.id)
        db.add(cat)
        db.commit()
        db.refresh(cat)

    # 3. Criar Produto
    prod = db.query(Product).filter(Product.category_id == cat.id).first()
    if not prod:
        prod = Product(
            name="X-Bacon",
            price=Decimal("25.00"),
            category_id=cat.id,
            is_available=True
        )
        db.add(prod)

    # 4. Criar Mesa
    table = db.query(Table).filter(Table.company_id == company.id, Table.table_number == 1).first()
    if not table:
        table = Table(
            table_number=1,
            company_id=company.id,
            qr_token="token-seguro-mesa-1",
            is_active=True
        )
        db.add(table)

    db.commit()
    db.close()
    print("✨ Seed finalizado com sucesso.")

if __name__ == "__main__":
    seed()

