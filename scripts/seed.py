import sys
import os
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import (
    Company, Table, Category, Product, PlanTier, OptionGroup, Option, 
    Order, OrderItem, ServiceRequest, CustomerWallet, TableSession, Ingredient, ProductRecipe, Employee, UserRole
)
from app.core.security import get_password_hash

def seed_data():
    db: Session = SessionLocal()
    
    print("🗑️  Limpando banco de dados (Drop All)...")
    Base.metadata.drop_all(bind=engine)
    
    print("Hz  Recriando tabelas (Create All)...")
    Base.metadata.create_all(bind=engine)

    print("🌱 Criando dados iniciais...")

    # 1. Empresa
    company = Company(
        name="Hamburgueria do Zé",
        slug="hamburgueria-ze",
        owner_email="admin@mesaflow.com",
        password_hash=get_password_hash("123456"),
        plan_tier=PlanTier.PRO,
        primary_color="#ea580c",
        pix_key="07774629661",
        loyalty_percentage=10.00
    )
    db.add(company)
    db.commit()
    db.refresh(company)

    # 2. Mesas
    tables = [
        Table(company_id=company.id, table_number=1, qr_token="token-seguro-mesa-1", position_x=10, position_y=10),
        Table(company_id=company.id, table_number=2, qr_token="token-seguro-mesa-2", position_x=30, position_y=10),
        Table(company_id=company.id, table_number=3, qr_token="token-seguro-mesa-3", position_x=50, position_y=10),
        Table(company_id=company.id, table_number=4, qr_token="token-seguro-mesa-4", position_x=10, position_y=40),
        Table(company_id=company.id, table_number=5, qr_token="token-seguro-mesa-5", position_x=30, position_y=40),
    ]
    db.add_all(tables)
    
    # 3. Categorias
    cat_lanches = Category(company_id=company.id, name="Lanches", order_index=1)
    cat_bebidas = Category(company_id=company.id, name="Bebidas", order_index=2)
    
    # Categoria Agendada (Happy Hour) - Só funciona das 17h às 20h
    cat_happy = Category(
        company_id=company.id, 
        name="Happy Hour", 
        order_index=3,
        availability_days=[1, 2, 3, 4, 5], # Seg-Sex
        start_time="17:00:00",
        end_time="20:00:00"
    )
    
    db.add_all([cat_lanches, cat_bebidas, cat_happy])
    db.commit()

    # 4. Produtos
    xbacon = Product(
        category_id=cat_lanches.id,
        name="X-Bacon",
        description="Pão, carne, queijo e bacon.",
        price=28.90,
        image_url="https://placehold.co/600x400/png?text=X-Bacon",
        track_stock=False,
        station="kitchen",
        tags=["promo", "carne"]
    )
    db.add(xbacon)

    coca = Product(
        category_id=cat_bebidas.id,
        name="Coca-Cola",
        description="Lata 350ml",
        price=6.00,
        image_url="https://placehold.co/600x400/png?text=Coca",
        track_stock=True,
        stock_quantity=50,
        station="bar",
        tags=["gelada"]
    )
    db.add(coca)
    
    batata = Product(
        category_id=cat_lanches.id,
        name="Batata Frita",
        description="Porção individual crocante.",
        price=12.00,
        image_url="https://placehold.co/600x400/png?text=Fritas",
        track_stock=False,
        station="kitchen",
        tags=["vegano", "sem-gluten"]
    )
    db.add(batata)
    
    chopp = Product(
        category_id=cat_happy.id,
        name="Chopp 500ml",
        description="Dobro no Happy Hour!",
        price=8.00,
        image_url="https://placehold.co/600x400/png?text=Chopp",
        station="bar",
        tags=["alcool"]
    )
    db.add(chopp)
    
    db.commit()

    # 5. Recomendações
    xbacon.recommendations.append(coca)
    xbacon.recommendations.append(batata)
    db.commit()

    # 6. Opções
    grp_ponto = OptionGroup(product_id=xbacon.id, name="Ponto da Carne", min_selection=1, max_selection=1)
    db.add(grp_ponto)
    db.commit()
    
    db.add(Option(group_id=grp_ponto.id, name="Ao Ponto", price=0))
    db.add(Option(group_id=grp_ponto.id, name="Bem Passado", price=0))

    # 7. Carteira de Teste
    wallet = CustomerWallet(
        company_id=company.id,
        customer_phone="11999999999",
        balance=15.00
    )
    db.add(wallet)
    
    # 8. Insumos (Ficha Técnica)
    ing_carne = Ingredient(company_id=company.id, name="Carne Moída", unit="kg", current_stock=10.000, cost_per_unit=35.00)
    ing_pao = Ingredient(company_id=company.id, name="Pão de Hambúrguer", unit="un", current_stock=50.000, cost_per_unit=1.50)
    ing_bacon = Ingredient(company_id=company.id, name="Bacon Fatiado", unit="kg", current_stock=2.000, cost_per_unit=45.00)
    
    db.add_all([ing_carne, ing_pao, ing_bacon])
    db.commit()
    
    # 9. Receita do X-Bacon
    db.add(ProductRecipe(product_id=xbacon.id, ingredient_id=ing_carne.id, quantity_required=0.180))
    db.add(ProductRecipe(product_id=xbacon.id, ingredient_id=ing_pao.id, quantity_required=1.000))
    db.add(ProductRecipe(product_id=xbacon.id, ingredient_id=ing_bacon.id, quantity_required=0.020))
    
    # 10. Funcionário de Teste (Cozinha)
    chef = Employee(
        company_id=company.id,
        name="Chef Jacquin",
        email="chef@mesaflow.com",
        password_hash=get_password_hash("123456"),
        role=UserRole.KITCHEN
    )
    db.add(chef)
    
    db.commit()

    print("✅ Banco de dados resetado e populado com sucesso!")
    print("   - Admin: admin@mesaflow.com / 123456")
    print("   - Chef: chef@mesaflow.com / 123456")
    print("   - Link Mesa 1: http://localhost:3000/hamburgueria-ze/menu?mesa=1&token=token-seguro-mesa-1")
    
    db.close()

if __name__ == "__main__":
    seed_data()