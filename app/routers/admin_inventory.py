from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Company, Ingredient, Product, ProductRecipe
from app.schemas import IngredientCreate, IngredientResponse, ProductRecipeUpdate
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/ingredients", response_model=List[IngredientResponse])
def get_ingredients(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    return db.query(Ingredient).filter(Ingredient.company_id == current_user.id).all()

@router.post("/ingredients", response_model=IngredientResponse, status_code=201)
def create_ingredient(
    data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    new_ingredient = Ingredient(
        company_id=current_user.id,
        name=data.name,
        unit=data.unit,
        current_stock=data.current_stock,
        min_stock_alert=data.min_stock_alert,
        cost_per_unit=data.cost_per_unit
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

@router.patch("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.company_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    ingredient.name = data.name
    ingredient.unit = data.unit
    ingredient.current_stock = data.current_stock
    ingredient.min_stock_alert = data.min_stock_alert
    ingredient.cost_per_unit = data.cost_per_unit
    
    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.company_id == current_user.id
    ).first()
    
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    db.delete(ingredient)
    db.commit()
    return None

@router.post("/recipes", status_code=200)
def update_product_recipe(
    data: ProductRecipeUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    # Verificar se o produto pertence à empresa
    product = db.query(Product).join(Company).filter(
        Product.id == data.product_id,
        Company.id == current_user.id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Limpar receita anterior
    db.query(ProductRecipe).filter(ProductRecipe.product_id == data.product_id).delete()
    
    # Adicionar novos itens
    for item in data.ingredients:
        # Verificar se ingrediente existe e pertence à empresa
        ing = db.query(Ingredient).filter(
            Ingredient.id == item.ingredient_id,
            Ingredient.company_id == current_user.id
        ).first()
        
        if ing:
            new_recipe_item = ProductRecipe(
                product_id=data.product_id,
                ingredient_id=item.ingredient_id,
                quantity_required=item.quantity_required
            )
            db.add(new_recipe_item)
            
    db.commit()
    return {"message": "Ficha técnica atualizada"}