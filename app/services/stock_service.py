from sqlalchemy.orm import Session
from app.models import Product, Ingredient, ProductRecipe, OrderItem
from decimal import Decimal

class StockService:
    def deduct_stock_for_order(self, db: Session, items: list[OrderItem]):
        """
        Baixa o estoque dos ingredientes baseada na ficha técnica dos produtos vendidos.
        """
        for item in items:
            # Buscar receita do produto
            recipes = db.query(ProductRecipe).filter(ProductRecipe.product_id == item.product_id).all()
            
            for recipe in recipes:
                ingredient = db.query(Ingredient).filter(Ingredient.id == recipe.ingredient_id).with_for_update().first()
                
                if ingredient:
                    # Quantidade total a baixar = Qtd do Pedido * Qtd da Receita
                    total_deduct = Decimal(item.quantity) * recipe.quantity_required
                    ingredient.current_stock -= total_deduct
                    
                    # Opcional: Logar se estoque ficar negativo ou abaixo do mínimo
                    if ingredient.current_stock < 0:
                        print(f"⚠️ ALERTA: Estoque negativo para {ingredient.name} ({ingredient.current_stock})")
        
        db.commit()