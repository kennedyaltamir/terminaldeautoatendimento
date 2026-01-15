
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 01:35:00

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from app.schemas.core import Monetary, OptionalMonetary

# --- SUPPLIER SCHEMAS ---

class SupplierCreate(BaseModel):
    name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class SupplierResponse(SupplierCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- INGREDIENT SCHEMAS ---

class IngredientBase(BaseModel):
    name: str
    unit: str = "un"  # kg, g, l, ml, un
    current_stock: float = 0.0
    min_stock_alert: float = 0.0
    cost_per_unit: Monetary = 0
    supplier_id: Optional[int] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int
    supplier: Optional[SupplierResponse] = None
    model_config = ConfigDict(from_attributes=True)

# --- RECIPE SCHEMAS ---

class RecipeItemCreate(BaseModel):
    ingredient_id: int
    quantity_required: float

class ProductRecipeUpdate(BaseModel):
    product_id: int
    ingredients: List[RecipeItemCreate]

# --- SHOPPING LIST SCHEMAS ---

class ShoppingListItem(BaseModel):
    ingredient_name: str
    current_stock: float
    min_stock: float
    unit: str
    deficit: float
    supplier_name: str

class ShoppingListResponse(BaseModel):
    items: List[ShoppingListItem]

