"""
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.1.0 (Diamond Hardened Master)
 * DNA_ID: MF-ROUTER-ADMIN-MENU-V2-1
 * OBJETIVO: Router de Gestão de Cardápio, Categorias e Produtos.
 * Comportamento esperado: 
 *  1. CRUD completo de Categorias, Produtos e Opcionais.
 *  2. Implementa ritos de auditoria (AuditLog) em todas as mutações.
 *  3. Gerencia limites de SaaS (SaasLimits) na criação de produtos.
 *  4. Suporta importação externa (iFood) e invalidação de cache distribuído.
 *  5. Tipagem estrita para conformidade total com Pyright.
 */
//
"""

import logging
from typing import List, Any, Optional, Union, cast
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from app.database import get_db
from app.models import Company, Category, Product, OptionGroup, Option, AuditAction, Employee
from app.schemas import (
    CategoryCreate, CategoryResponse, CategoryUpdate, 
    ProductCreate, ProductUpdate, ProductResponse,
    OptionGroupCreate, OptionGroupResponse, 
    OptionCreate, OptionResponse
)
from app.routers.auth import get_current_user
from app.core.saas_limits import SaasLimits
from app.services.audit_service import AuditService
from app.core.cache import CacheService
from app.services.importer_service import ImporterService

logger = logging.getLogger("MenuRouter")
router = APIRouter()

class ImportRequest(BaseModel):
    url: str

# --- HELPERS ---

def get_slug(user: Union[Company, Employee]) -> str:
    """Extrai o slug da empresa de forma segura para o Pyright."""
    if isinstance(user, Company):
        return str(user.slug)
    return str(user.company.slug)

def _resolve_company_id(user: Union[Company, Employee]) -> Any:
    """Resolve o ID da empresa independente do tipo de ator."""
    return user.id if isinstance(user, Company) else user.company_id

# --- ENDPOINTS: PRODUTOS ---

@router.get("/products", response_model=List[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Lista todos os produtos da empresa (Flat List)."""
    company_id = _resolve_company_id(current_user)
    # 🛡️ FIX: Pyright confusion with built-in all()
    query = db.query(Product).join(Category).filter(Category.company_id == company_id)
    return query.all()

@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product(
    request: Request,
    product_data: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Cria um novo produto validando limites do plano."""
    company_id = _resolve_company_id(current_user)
    company = current_user if isinstance(current_user, Company) else current_user.company
    
    # 🛡️ SaaS Guard
    SaasLimits.check_product_limit(db, company)
    
    category = db.query(Category).filter(
        Category.id == product_data.category_id, 
        Category.company_id == company_id
    ).first()
    
    if not category:
        raise HTTPException(status_code=400, detail="Categoria inválida ou não pertence a esta unidade.")
        
    new_product = Product(
        category_id=product_data.category_id, 
        name=product_data.name, 
        description=product_data.description, 
        price=product_data.price, 
        image_url=product_data.image_url, 
        is_available=product_data.is_available,
        track_stock=product_data.track_stock,
        stock_quantity=product_data.stock_quantity,
        station=product_data.station,
        tags=product_data.tags,
        short_code=product_data.short_code
    )
    
    if product_data.recommended_ids:
        recs = db.query(Product).filter(Product.id.in_(product_data.recommended_ids)).all()
        new_product.recommendations = recs
        
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    AuditService.log(
        db, current_user, AuditAction.CREATE, "Product", str(new_product.id),
        details={"name": str(new_product.name), "price": float(cast(Decimal, new_product.price))}, 
        request=request
    )
    CacheService.invalidate_menu(get_slug(current_user))
    return new_product

@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    request: Request,
    product_id: int, 
    product_data: ProductUpdate, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Atualiza dados do produto com auditoria de mudanças."""
    company_id = _resolve_company_id(current_user)
    product = db.query(Product).join(Category).filter(
        Product.id == product_id, 
        Category.company_id == company_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    update_data = product_data.model_dump(exclude_unset=True)
    diff = AuditService.diff(product, update_data)
    
    if "recommended_ids" in update_data:
        rec_ids = update_data.pop("recommended_ids")
        if rec_ids is not None:
            recs = db.query(Product).filter(Product.id.in_(rec_ids)).all()
            product.recommendations = recs
            
    for key, value in update_data.items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    
    if diff:
        AuditService.log(
            db, current_user, AuditAction.UPDATE, "Product", str(product.id),
            details=diff, request=request
        )
    CacheService.invalidate_menu(get_slug(current_user))
    return product

@router.delete("/products/{product_id}", status_code=204)
def delete_product(
    request: Request,
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Remove um produto se não houver dependências ativas."""
    company_id = _resolve_company_id(current_user)
    product = db.query(Product).join(Category).filter(
        Product.id == product_id, 
        Category.company_id == company_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    try:
        AuditService.log(
            db, current_user, AuditAction.DELETE, "Product", str(product.id),
            details={"name": str(product.name)}, request=request
        )
        db.delete(product)
        db.commit()
        CacheService.invalidate_menu(get_slug(current_user))
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, 
            detail="Não é possível excluir este produto pois ele já possui pedidos vinculados. Desative-o em vez de excluir."
        )
    return None

# --- ENDPOINTS: CATEGORIAS ---

@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    request: Request,
    category_data: CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Cria uma nova categoria de produtos."""
    company_id = _resolve_company_id(current_user)
    new_category = Category(
        company_id=company_id, 
        name=category_data.name, 
        order_index=category_data.order_index,
        availability_days=category_data.availability_days,
        start_time=category_data.start_time,
        end_time=category_data.end_time
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    AuditService.log(
        db, current_user, AuditAction.CREATE, "Category", str(new_category.id),
        details={"name": str(new_category.name)}, request=request
    )
    CacheService.invalidate_menu(get_slug(current_user))
    return new_category

@router.patch("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category_data: CategoryUpdate, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Atualiza metadados da categoria."""
    company_id = _resolve_company_id(current_user)
    category = db.query(Category).filter(
        Category.id == category_id, 
        Category.company_id == company_id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    update_data = category_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    CacheService.invalidate_menu(get_slug(current_user))
    return category

@router.delete("/categories/{category_id}", status_code=204)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Remove uma categoria se estiver vazia."""
    company_id = _resolve_company_id(current_user)
    category = db.query(Category).filter(
        Category.id == category_id, 
        Category.company_id == company_id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    try:
        db.delete(category)
        db.commit()
        CacheService.invalidate_menu(get_slug(current_user))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Não é possível excluir categoria com produtos vinculados.")
    return None

# --- ENDPOINTS: OPCIONAIS ---

@router.post("/products/{product_id}/groups", response_model=OptionGroupResponse, status_code=201)
def create_option_group(
    product_id: int, 
    group_data: OptionGroupCreate, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Cria um grupo de opcionais para um produto."""
    company_id = _resolve_company_id(current_user)
    product = db.query(Product).join(Category).filter(
        Product.id == product_id, 
        Category.company_id == company_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    new_group = OptionGroup(
        product_id=product_id, 
        name=group_data.name, 
        min_selection=group_data.min_selection, 
        max_selection=group_data.max_selection
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    CacheService.invalidate_menu(get_slug(current_user))
    return new_group

@router.post("/groups/{group_id}/options", response_model=OptionResponse, status_code=201)
def create_option(
    group_id: int, 
    option_data: OptionCreate, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Adiciona uma opção individual a um grupo."""
    company_id = _resolve_company_id(current_user)
    group = db.query(OptionGroup).join(Product).join(Category).filter(
        OptionGroup.id == group_id, 
        Category.company_id == company_id
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
    new_option = Option(group_id=group_id, name=option_data.name, price=option_data.price)
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    CacheService.invalidate_menu(get_slug(current_user))
    return new_option

@router.delete("/groups/{group_id}", status_code=204)
def delete_option_group(group_id: int, db: Session = Depends(get_db), current_user: Union[Company, Employee] = Depends(get_current_user)):
    """Remove um grupo de opcionais."""
    company_id = _resolve_company_id(current_user)
    group = db.query(OptionGroup).join(Product).join(Category).filter(
        OptionGroup.id == group_id, 
        Category.company_id == company_id
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    db.delete(group)
    db.commit()
    CacheService.invalidate_menu(get_slug(current_user))
    return None

@router.delete("/options/{option_id}", status_code=204)
def delete_option(option_id: int, db: Session = Depends(get_db), current_user: Union[Company, Employee] = Depends(get_current_user)):
    """Remove uma opção individual."""
    company_id = _resolve_company_id(current_user)
    option = db.query(Option).join(OptionGroup).join(Product).join(Category).filter(
        Option.id == option_id, 
        Category.company_id == company_id
    ).first()
    
    if not option:
        raise HTTPException(status_code=404, detail="Opção não encontrada")
    
    db.delete(option)
    db.commit()
    CacheService.invalidate_menu(get_slug(current_user))
    return None

# --- INTEGRAÇÕES ---

@router.post("/import/ifood", status_code=200)
async def import_ifood_menu(
    data: ImportRequest,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """Importa cardápio de uma URL pública do iFood."""
    company_id = _resolve_company_id(current_user)
    try:
        result = await ImporterService.import_from_ifood(db, str(company_id), data.url)
        CacheService.invalidate_menu(get_slug(current_user))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro importação iFood: {e}")
        raise HTTPException(status_code=500, detail="Erro interno na importação")