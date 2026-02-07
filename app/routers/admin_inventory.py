"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.2.0 (Tenant ID Fix)
 * DNA_ID: MF-ROUTER-INVENTORY-V1-2
 * OBJETIVO: Router de Inventário com resolução robusta de Tenant ID.
 * CORREÇÃO: Resolve o erro 'invalid input syntax for type uuid' normalizando
 * a obtenção do company_id independente se o usuário é Owner ou Employee.
 */
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from typing import List, Union
from app.database import get_db
from app.models import Company, Ingredient, Product, ProductRecipe, Supplier, Employee
from app.schemas import IngredientCreate, IngredientResponse, ProductRecipeUpdate, SupplierCreate, SupplierResponse, ShoppingListResponse, ShoppingListItem
from app.routers.auth import get_current_user
from app.services.purchase_service import PurchaseService

router = APIRouter()

# --- HELPER: RESOLUÇÃO DE TENANT ---
def get_company_id(user: Union[Company, Employee]) -> str:
    """
    Resolve o ID da empresa.
    Se for Employee, usa user.company_id.
    Se for Company (Owner), usa user.id.
    """
    if hasattr(user, "company_id") and user.company_id:
        return str(user.company_id)
    return str(user.id)

# --- INGREDIENTES ---
@router.get("/ingredients", response_model=List[IngredientResponse])
def get_ingredients(
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    return db.query(Ingredient).filter(Ingredient.company_id == company_id).all()

@router.post("/ingredients", response_model=IngredientResponse, status_code=201)
def create_ingredient(
    data: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    new_ingredient = Ingredient(
        company_id=company_id,
        name=data.name,
        unit=data.unit,
        current_stock=data.current_stock,
        min_stock_alert=data.min_stock_alert,
        cost_per_unit=data.cost_per_unit,
        supplier_id=data.supplier_id
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
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.company_id == company_id
    ).first()
    
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    ingredient.name = data.name
    ingredient.unit = data.unit
    ingredient.current_stock = data.current_stock
    ingredient.min_stock_alert = data.min_stock_alert
    ingredient.cost_per_unit = data.cost_per_unit
    ingredient.supplier_id = data.supplier_id
    
    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id,
        Ingredient.company_id == company_id
    ).first()
    
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    try:
        db.delete(ingredient)
        db.commit()
    except IntegrityError:
        db.rollback()
        # 🛡️ TRATAMENTO DE ERRO: Retorna 409 (Conflito) em vez de crashar
        raise HTTPException(
            status_code=409, 
            detail="Não é possível excluir: este insumo faz parte de uma Ficha Técnica ativa."
        )
    return None

# --- LISTA DE COMPRAS & ORDENS ---
@router.get("/shopping-list", response_model=ShoppingListResponse)
def get_shopping_list(
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    # Busca ingredientes com estoque baixo
    low_stock_ingredients = db.query(Ingredient).options(selectinload(Ingredient.supplier)).filter(
        Ingredient.company_id == company_id,
        Ingredient.current_stock <= Ingredient.min_stock_alert
    ).all()
    
    items = []
    for ing in low_stock_ingredients:
        deficit = ing.min_stock_alert - ing.current_stock
        if deficit < 0: deficit = 0
        
        items.append(ShoppingListItem(
            ingredient_name=ing.name,
            current_stock=ing.current_stock,
            min_stock=ing.min_stock_alert,
            unit=ing.unit,
            deficit=deficit,
            supplier_name=ing.supplier.name if ing.supplier else "Sem Fornecedor"
        ))
        
    return {"items": items}

@router.get("/purchase-orders/preview")
def preview_purchase_orders(
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Retorna sugestões de compra agrupadas por fornecedor"""
    company_id = get_company_id(current_user)
    return PurchaseService.generate_purchase_suggestion(db, company_id)

@router.get("/purchase-orders/{supplier_id}/print")
def print_purchase_order(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Gera um HTML de impressão para a ordem de compra"""
    company_id = get_company_id(current_user)
    all_orders = PurchaseService.generate_purchase_suggestion(db, company_id)
    
    # Lógica simplificada para encontrar o fornecedor na lista gerada
    supplier_name = "Sem Fornecedor"
    if supplier_id > 0:
        sup = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.company_id == company_id).first()
        if not sup: raise HTTPException(404, "Fornecedor não encontrado")
        supplier_name = sup.name
        
    order_data = next((o for o in all_orders if o["supplier_name"] == supplier_name), None)
    
    if not order_data:
        return Response(content="<h1>Nenhum item para comprar deste fornecedor.</h1>", media_type="text/html")
    
    # Para o template HTML, precisamos do nome da empresa.
    # Se for Employee, buscamos a empresa. Se for Company, usamos direto.
    company_name = current_user.name
    if hasattr(current_user, "company"):
        company_name = current_user.company.name
        
    # Mock de objeto company apenas com o nome para o serviço
    mock_company = type('obj', (object,), {'name': company_name})
    
    html_content = PurchaseService.generate_html_order(mock_company, order_data)
    return Response(content=html_content, media_type="text/html")
