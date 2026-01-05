import sys
import os
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    Company, Table, Category, Product, PlanTier, OptionGroup, Option, 
    Order, OrderItem, ServiceRequest, CustomerWallet, TableSession, Ingredient, ProductRecipe, Employee, UserRole, Supplier, CompanySegment
)
from app.core.security import get_password_hash

def seed_data():
    db: Session = SessionLocal()
    
    print("🗑️  Limpando banco de dados (Drop All)...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️  Recriando tabelas...")
    Base.metadata.create_all(bind=engine)

    print("🌱 Criando dados iniciais...")

    # 1. Empresa Principal (Gastro)
    company = Company(
        name="Hamburgueria do Zé",
        slug="hamburgueria-ze",
        owner_email="admin@mesaflow.com",
        password_hash=get_password_hash("123456"),
        plan_tier=PlanTier.PRO,
        primary_color="#ea580c",
        pix_key="07774629661",
        whatsapp_number="5511999999999",
        loyalty_percentage=Decimal("10.00"),
        subscription_status="active",
        segment=CompanySegment.GASTRO
    )
    db.add(company)
    
    # 2. Empresa Demo Hotel
    hotel = Company(
        name="Grand Plaza Hotel",
        slug="demo-hotel",
        owner_email="hotel@demo.com",
        password_hash=get_password_hash("123456"),
        plan_tier=PlanTier.ENTERPRISE,
        primary_color="#3b82f6", # Azul
        segment=CompanySegment.HOTEL
    )
    db.add(hotel)

    # 3. Empresa Demo Evento
    arena = Company(
        name="Arena Show",
        slug="demo-evento",
        owner_email="evento@demo.com",
        password_hash=get_password_hash("123456"),
        plan_tier=PlanTier.ENTERPRISE,
        primary_color="#8b5cf6", # Roxo
        segment=CompanySegment.EVENT
    )
    db.add(arena)

    # 4. Empresa Demo Corporativo
    corp = Company(
        name="Tech Hub Café",
        slug="demo-corp",
        owner_email="corp@demo.com",
        password_hash=get_password_hash("123456"),
        plan_tier=PlanTier.PRO,
        primary_color="#10b981", # Verde
        segment=CompanySegment.CORP
    )
    db.add(corp)
    
    db.commit()
    db.refresh(company)
    db.refresh(hotel)
    db.refresh(arena)
    db.refresh(corp)

    # --- POPULAR GASTRO (Zé) ---
    # Fornecedores
    sup_acougue = Supplier(company_id=company.id, name="Açougue do Zé", phone="11999990001")
    db.add(sup_acougue)
    db.commit()

    # Mesas
    tables = [Table(company_id=company.id, table_number=i, qr_token=f"token-seguro-mesa-{i}") for i in range(1, 6)]
    db.add_all(tables)
    
    # Categorias
    cat_lanches = Category(company_id=company.id, name="Lanches", order_index=1)
    cat_bebidas = Category(company_id=company.id, name="Bebidas", order_index=2)
    db.add_all([cat_lanches, cat_bebidas])
    db.commit()

    # Produtos
    xbacon = Product(category_id=cat_lanches.id, name="X-Bacon", price=Decimal("28.90"), image_url="https://placehold.co/600x400/png?text=X-Bacon", station="kitchen")
    coca = Product(category_id=cat_bebidas.id, name="Coca-Cola", price=Decimal("6.00"), image_url="https://placehold.co/600x400/png?text=Coca", station="bar")
    db.add_all([xbacon, coca])
    db.commit()

    # --- POPULAR HOTEL ---
    cat_room = Category(company_id=hotel.id, name="Room Service 24h", order_index=1)
    cat_pool = Category(company_id=hotel.id, name="Bar da Piscina", order_index=2)
    db.add_all([cat_room, cat_pool])
    db.commit()
    
    db.add(Product(category_id=cat_room.id, name="Club Sandwich", price=Decimal("45.00"), description="Clássico sanduíche de hotel", station="kitchen"))
    db.add(Product(category_id=cat_room.id, name="Toalha Extra", price=Decimal("0.00"), description="Solicitar na recepção", station="other"))
    db.add(Product(category_id=cat_pool.id, name="Caipirinha", price=Decimal("30.00"), station="bar"))
    
    # Quartos (Mesas)
    db.add(Table(company_id=hotel.id, table_number=101, qr_token="room-101"))
    db.add(Table(company_id=hotel.id, table_number=102, qr_token="room-102"))
    db.commit()

    # --- POPULAR EVENTO ---
    cat_show = Category(company_id=arena.id, name="Bebidas", order_index=1)
    db.add(cat_show)
    db.commit()
    db.add(Product(category_id=cat_show.id, name="Cerveja Lata", price=Decimal("15.00"), station="bar"))
    db.add(Product(category_id=cat_show.id, name="Água", price=Decimal("8.00"), station="bar"))
    
    # Assentos
    db.add(Table(company_id=arena.id, table_number=1, qr_token="seat-a1")) # Setor A, Cad 1

    # --- POPULAR CORP ---
    cat_coffee = Category(company_id=corp.id, name="Coffee Break", order_index=1)
    db.add(cat_coffee)
    db.commit()
    db.add(Product(category_id=cat_coffee.id, name="Espresso", price=Decimal("5.00"), station="bar"))
    db.add(Product(category_id=cat_coffee.id, name="Pão de Queijo", price=Decimal("6.00"), station="kitchen"))

    print("✅ Banco de dados resetado e populado com sucesso!")
    db.close()

if __name__ == "__main__": 
    seed_data()