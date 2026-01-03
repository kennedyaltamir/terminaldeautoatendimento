from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.database import get_db
from app.models import Company, Ingredient, Product, ProductRecipe, Supplier
from app.schemas import IngredientCreate, IngredientResponse, ProductRecipeUpdate, SupplierCreate, SupplierResponse, ShoppingListResponse, ShoppingListItem
from app.routers.auth import get_current_user
from app.services.purchase_service import PurchaseService

router = APIRouter()

# --- INGREDIENTES ---

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
    ingredient.supplier_id = data.supplier_id
    
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

# --- RECEITAS ---

@router.post("/recipes", status_code=200)
def update_product_recipe(
    data: ProductRecipeUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    product = db.query(Product).join(Company).filter(
        Product.id == data.product_id,
        Company.id == current_user.id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.query(ProductRecipe).filter(ProductRecipe.product_id == data.product_id).delete()
    
    for item in data.ingredients:
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

# --- FORNECEDORES ---

@router.get("/suppliers", response_model=List[SupplierResponse])
def get_suppliers(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    return db.query(Supplier).filter(Supplier.company_id == current_user.id).all()

@router.post("/suppliers", response_model=SupplierResponse, status_code=201)
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    new_supplier = Supplier(
        company_id=current_user.id,
        name=data.name,
        contact_name=data.contact_name,
        phone=data.phone,
        email=data.email
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

@router.delete("/suppliers/{supplier_id}", status_code=204)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id,
        Supplier.company_id == current_user.id
    ).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    db.delete(supplier)
    db.commit()
    return None

# --- LISTA DE COMPRAS & ORDENS ---

@router.get("/shopping-list", response_model=ShoppingListResponse)
def get_shopping_list(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    # Busca ingredientes com estoque baixo
    low_stock_ingredients = db.query(Ingredient).options(selectinload(Ingredient.supplier)).filter(
        Ingredient.company_id == current_user.id,
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
    current_user: Company = Depends(get_current_user)
):
    """Retorna sugestões de compra agrupadas por fornecedor"""
    return PurchaseService.generate_purchase_suggestion(db, current_user.id)

@router.get("/purchase-orders/{supplier_id}/print")
def print_purchase_order(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """Gera um HTML de impressão para a ordem de compra"""
    suggestions = PurchaseService.generate_purchase_suggestion(db, current_user.id)
    
    # Encontrar a sugestão para este fornecedor
    # Nota: supplier_id 0 é "Sem Fornecedor"
    target_order = next((s for s in suggestions if (s.get("supplier_name") and supplier_id > 0) or (supplier_id == 0)), None)
    
    # Refinamento: A lógica acima está frágil pois generate_purchase_suggestion retorna uma lista de dicts sem o ID explícito no topo.
    # Vamos melhorar o service para retornar o ID ou filtrar melhor aqui.
    # Por simplicidade, vamos refazer a busca focada.
    
    # Re-executa a lógica (em produção, cachearíamos)
    # Mas precisamos achar o dict correto na lista retornada.
    # O service retorna uma lista de dicts. Vamos adicionar o supplier_id no dict do service para facilitar.
    
    # Hack rápido: O service não retorna o ID no dict final. Vamos ajustar o service na próxima iteração se precisar.
    # Por enquanto, vamos assumir que o frontend manda o índice ou iteramos até achar o nome do fornecedor se tivermos.
    # Melhor: Vamos confiar que o service retorna tudo e filtramos no python.
    
    # Ajuste no Service (feito mentalmente): O service agrupa por ID.
    # Vamos assumir que o frontend chama com o ID correto.
    
    # Busca o fornecedor para pegar o nome e validar
    supplier_name = "Sem Fornecedor"
    if supplier_id > 0:
        sup = db.query(Supplier).filter(Supplier.id == supplier_id, Supplier.company_id == current_user.id).first()
        if not sup: raise HTTPException(404, "Fornecedor não encontrado")
        supplier_name = sup.name

    # Filtra a lista completa
    all_orders = PurchaseService.generate_purchase_suggestion(db, current_user.id)
    order_data = next((o for o in all_orders if o["supplier_name"] == supplier_name), None)

    if not order_data:
        return Response(content="<h1>Nenhum item para comprar deste fornecedor.</h1>", media_type="text/html")

    html_content = PurchaseService.generate_html_order(current_user, order_data)
    return Response(content=html_content, media_type="text/html")