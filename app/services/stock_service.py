# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from sqlalchemy.orm import Session
from app.models import Product, Ingredient, ProductRecipe, OrderItem, Company
from decimal import Decimal
from app.services.whatsapp_service import WhatsAppService
from fastapi import BackgroundTasks, HTTPException

class StockService:
    def __init__(self):
        self.whatsapp = WhatsAppService()

    def deduct_stock_for_order(self, db: Session, items: list[OrderItem], background_tasks: BackgroundTasks):
        """
        Baixa o estoque dos ingredientes de forma SÍNCRONA dentro da transação do pedido.
        Se faltar estoque, lança exceção e aborta o pedido (Rollback).
        A notificação (WhatsApp) permanece assíncrona.
        """
        # Cache para evitar queries repetidas do mesmo ingrediente no loop
        ingredients_cache = {}

        for item in items:
            # Busca receitas vinculadas ao produto
            recipes = db.query(ProductRecipe).filter(ProductRecipe.product_id == item.product_id).all()
            
            # Se não tem receita (produto simples), decrementa o produto direto se track_stock=True
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product and product.track_stock:
                if product.stock_quantity < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Estoque insuficiente para: {product.name}")
                product.stock_quantity -= item.quantity
                
                # Regra 86: Se zerou, desativa
                if product.stock_quantity <= 0:
                    product.is_available = False

            # Processa ingredientes da ficha técnica
            for recipe in recipes:
                ing_id = recipe.ingredient_id
                
                if ing_id not in ingredients_cache:
                    # Lock de linha (with_for_update) para evitar Race Condition
                    ingredients_cache[ing_id] = db.query(Ingredient).filter(Ingredient.id == ing_id).with_for_update().first()
                
                ingredient = ingredients_cache[ing_id]
                
                if ingredient:
                    required_amount = Decimal(str(item.quantity)) * recipe.quantity_required
                    
                    # Validação Rígida de Estoque
                    if ingredient.current_stock < required_amount:
                         raise HTTPException(
                             status_code=400, 
                             detail=f"Ingrediente esgotado: {ingredient.name} (Necessário: {required_amount}, Atual: {ingredient.current_stock})"
                         )

                    ingredient.current_stock -= required_amount
                    
                    # Se atingiu nível crítico ou zero, agenda notificação e bloqueio
                    if ingredient.current_stock <= 0:
                        self._schedule_out_of_stock_handling(ingredient, background_tasks)

    def _schedule_out_of_stock_handling(self, ingredient: Ingredient, background_tasks: BackgroundTasks):
        """
        Agenda a tarefa de notificação e desativação em cascata.
        """
        background_tasks.add_task(self._handle_out_of_stock_async, ingredient.id, ingredient.name, ingredient.unit, str(ingredient.current_stock), ingredient.company_id)

    def _handle_out_of_stock_async(self, ingredient_id: int, name: str, unit: str, stock: str, company_id: str):
        """
        Worker assíncrono que roda após o commit do pedido.
        Reabre uma sessão para desativar produtos e notificar.
        """
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            # Busca produtos que usam este ingrediente
            affected_recipes = db.query(ProductRecipe).filter(ProductRecipe.ingredient_id == ingredient_id).all()
            affected_product_ids = [r.product_id for r in affected_recipes]
            
            product_names = []
            if affected_product_ids:
                products = db.query(Product).filter(Product.id.in_(affected_product_ids)).all()
                for prod in products:
                    if prod.is_available:
                        prod.is_available = False
                        product_names.append(prod.name)
                db.commit()
            
            # Notifica via WhatsApp
            company = db.query(Company).filter(Company.id == company_id).first()
            if company and company.whatsapp_number and product_names:
                import asyncio
                asyncio.run(self.whatsapp.notify_low_stock(
                    phone=company.whatsapp_number,
                    ingredient_name=name,
                    affected_products=product_names,
                    current_stock=float(stock),
                    unit=unit,
                    company_settings=company # Passa a empresa para pegar a config da API
                ))
        except Exception as e:
            print(f"Erro no worker de estoque: {e}")
        finally:
            db.close()
