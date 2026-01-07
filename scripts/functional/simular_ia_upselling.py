import sys
import os
import uuid
import random
from decimal import Decimal

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import Company, Category, Product, Order, OrderItem, OrderStatus, PaymentStatus
from app.services.recommendation_service import RecommendationService

def simular_ia():
    print("🧠 Iniciando Simulação de IA (Upselling)...")
    
    db = SessionLocal()
    unique_id = uuid.uuid4().hex[:6]
    
    # 1. Criar Cenário
    print("1. Criando Loja e Produtos de Teste...")
    company = Company(
        name=f"IA Burger {unique_id}", 
        slug=f"ia-{unique_id}", 
        owner_email=f"ia-{unique_id}@test.com"
    )
    db.add(company)
    db.commit()

    cat = Category(company_id=company.id, name="Lanches")
    db.add(cat)
    db.commit()

    # Produtos
    p_burger = Product(category_id=cat.id, name="X-Salada", price=20.00)
    p_fritas = Product(category_id=cat.id, name="Batata Frita", price=10.00)
    p_coca = Product(category_id=cat.id, name="Coca-Cola", price=5.00)
    p_agua = Product(category_id=cat.id, name="Água", price=3.00)
    
    db.add_all([p_burger, p_fritas, p_coca, p_agua])
    db.commit()

    print(f"   Produtos criados: {p_burger.name}, {p_fritas.name}, {p_coca.name}, {p_agua.name}")

    # 2. Gerar Histórico de Vendas (Bias)
    # Vamos criar um padrão forte: Quem compra Burger, compra Fritas e Coca.
    # Água é comprada aleatoriamente e raramente com Burger.
    
    print("2. Gerando 50 pedidos históricos com padrões de consumo...")
    
    for i in range(50):
        order = Order(
            company_id=company.id,
            total_amount=Decimal("0.00"),
            status=OrderStatus.DELIVERED, # Importante: IA só olha pedidos finalizados
            payment_status=PaymentStatus.PAID
        )
        db.add(order)
        db.commit()

        items = []
        
        # 80% das vezes pede Burger
        if random.random() < 0.8:
            items.append(OrderItem(order_id=order.id, product_id=p_burger.id, quantity=1, unit_price=20.00))
            
            # Se pediu Burger, 90% das vezes pede Fritas (Forte Correlação)
            if random.random() < 0.9:
                items.append(OrderItem(order_id=order.id, product_id=p_fritas.id, quantity=1, unit_price=10.00))
            
            # Se pediu Burger, 70% das vezes pede Coca (Média Correlação)
            if random.random() < 0.7:
                items.append(OrderItem(order_id=order.id, product_id=p_coca.id, quantity=1, unit_price=5.00))

        # 10% das vezes pede Água (Ruído)
        if random.random() < 0.1:
            items.append(OrderItem(order_id=order.id, product_id=p_agua.id, quantity=1, unit_price=3.00))

        if items:
            db.add_all(items)
            db.commit()

    print("   Histórico gerado.")

    # 3. Executar Motor de IA
    print("3. Executando RecommendationService...")
    links = RecommendationService.generate_recommendations(db, str(company.id), min_confidence=0.4)
    print(f"   IA gerou {links} conexões.")

    # 4. Validar Resultados
    print("4. Validando Recomendações para 'X-Salada'...")
    
    # Recarrega o produto para pegar as relações atualizadas
    db.refresh(p_burger)
    
    recs = p_burger.recommendations
    rec_names = [p.name for p in recs]
    
    print(f"   Recomendações encontradas: {rec_names}")

    if "Batata Frita" in rec_names:
        print("✅ SUCESSO: A IA aprendeu que Batata acompanha Burger!")
    else:
        print("❌ FALHA: Batata não foi recomendada (Confiança insuficiente ou erro).")

    if "Água" not in rec_names:
        print("✅ SUCESSO: A IA ignorou a Água (Baixa correlação).")
    else:
        print("⚠️ AVISO: Água foi recomendada (Verificar threshold).")

    db.close()

if __name__ == "__main__":
    simular_ia()
