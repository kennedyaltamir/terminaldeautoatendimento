from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, Category, Product, OptionGroup, Option, AuditAction
from app.schemas import (
    CategoryCreate, CategoryResponse, CategoryUpdate, ProductCreate, ProductUpdate, ProductResponse,
    OptionGroupCreate, OptionGroupResponse, OptionCreate, OptionResponse
)
from app.routers.auth import get_current_user
from app.core.saas_limits import SaasLimits
from app.services.audit_service import AuditService
from app.core.cache import CacheService # NOVO

router = APIRouter()

def get_slug(user: any) -> str:
    if isinstance(user, Company):
        return user.slug
    return user.company.slug

@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    request: Request,
    category_data: CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

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
        details={"name": new_category.name}, request=request
    )
    
    # Invalida Cache
    CacheService.invalidate_menu(get_slug(current_user))

    return new_category

@router.patch("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category_data: CategoryUpdate, 
    db: Session = Depends(get_db), 
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    category = db.query(Category).filter(Category.id == category_id, Category.company_id == company_id).first()
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
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    category = db.query(Category).filter(Category.id == category_id, Category.company_id == company_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(category)
    db.commit()
    CacheService.invalidate_menu(get_slug(current_user))
    return None

@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product(
    request: Request,
    product_data: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    company = current_user if isinstance(current_user, Company) else current_user.company
    SaasLimits.check_product_limit(db, company)

    category = db.query(Category).filter(Category.id == product_data.category_id, Category.company_id == company_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Categoria inválida")
    
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
        details={"name": new_product.name, "price": float(new_product.price)}, request=request
    )
    
    CacheService.invalidate_menu(get_slug(current_user))
    return new_product

@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    request: Request,
    product_id: int, 
    product_data: ProductUpdate, 
    db: Session = Depends(get_db), 
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    product = db.query(Product).join(Category).filter(Product.id == product_id, Category.company_id == company_id).first()
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
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    product = db.query(Product).join(Category).filter(Product.id == product_id, Category.company_id == company_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    AuditService.log(
        db, current_user, AuditAction.DELETE, "Product", str(product.id),
        details={"name": product.name}, request=request
    )

    db.delete(product)
    db.commit()
    CacheService.invalidate_menu(get_slug(current_user))
    return None

@router.post("/products/{product_id}/groups", response_model=OptionGroupResponse, status_code=201)
def create_option_group(product_id: int, group_data: OptionGroupCreate, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    product = db.query(Product).join(Category).filter(Product.id == product_id, Category.company_id == company_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    new_group = OptionGroup(product_id=product_id, name=group_data.name, min_selection=group_data.min_selection, max_selection=group_data.max_selection)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    CacheService.invalidate_menu(get_slug(current_user))
    return new_group

@router.post("/groups/{group_id}/options", response_model=OptionResponse, status_code=201)
def create_option(group_id: int, option_data: OptionCreate, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    group = db.query(OptionGroup).join(Product).join(Category).filter(OptionGroup.id == group_id, Category.company_id == company_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    new_option = Option(group_id=group_id, name=option_data.name, price=option_data.price)
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    CacheService.invalidate_menu(get_slug(current_user))
    return new_option

@router.delete("/groups/{group_id}", status_code=204)
def delete_option_group(group_id: int, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    group = db.query(OptionGroup).join(Product).join(Category).filter(OptionGroup.id == group_id, Category.company_id == company_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    db.delete(group)
    db.commit()
    CacheService.invalidate_menu(get_slug(current_user))
    return None

@router.delete("/options/{option_id}", status_code=204)
def delete_option(option_id: int, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    option = db.query(Option).join(OptionGroup).join(Product).join(Category).filter(Option.id == option_id, Category.company_id == company_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Opção não encontrada")
    db.delete(option)
    db.commit()
    CacheService.invalidate_menu(get_slug(current_user))
    return None
