from sqlalchemy.orm import Session
from app.models import Product, Ingredient, ProductRecipe, OrderItem, Company
from decimal import Decimal
from app.services.whatsapp_service import WhatsAppService
from fastapi import BackgroundTasks

class StockService:
    def __init__(self):
        self.whatsapp = WhatsAppService()

    def deduct_stock_for_order(self, db: Session, items: list[OrderItem], background_tasks: BackgroundTasks):
        """
        Baixa o estoque dos ingredientes e aplica a regra '86' (esgotar produto) se necessário.
        """
        for item in items:
            recipes = db.query(ProductRecipe).filter(ProductRecipe.product_id == item.product_id).all()
            
            for recipe in recipes:
                ingredient = db.query(Ingredient).filter(Ingredient.id == recipe.ingredient_id).with_for_update().first()
                
                if ingredient:
                    total_deduct = Decimal(str(item.quantity)) * recipe.quantity_required
                    ingredient.current_stock -= total_deduct
                    
                    if ingredient.current_stock <= 0:
                        self._handle_out_of_stock(db, ingredient, background_tasks)
        
        db.commit()

    def _handle_out_of_stock(self, db: Session, ingredient: Ingredient, background_tasks: BackgroundTasks):
        """
        Desativa produtos vinculados e agenda notificação via BackgroundTasks.
        """
        affected_recipes = db.query(ProductRecipe).filter(ProductRecipe.ingredient_id == ingredient.id).all()
        affected_product_ids = [r.product_id for r in affected_recipes]
        
        if not affected_product_ids:
            return

        products = db.query(Product).filter(Product.id.in_(affected_product_ids)).all()
        product_names = []
        for prod in products:
            prod.is_available = False
            product_names.append(prod.name)
        
        company = db.query(Company).filter(Company.id == ingredient.company_id).first()
        
        if company and company.whatsapp_number:
            background_tasks.add_task(
                self.whatsapp.notify_low_stock,
                phone=company.whatsapp_number,
                ingredient_name=ingredient.name,
                affected_products=product_names,
                current_stock=float(ingredient.current_stock),
                unit=ingredient.unit
            )