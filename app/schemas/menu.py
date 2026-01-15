# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 09:15:00

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any
from datetime import time
from app.schemas.core import Monetary, OptionalMonetary
from app.schemas.company import CompanyPublic

class OptionResponse(BaseModel):
    id: int
    name: str
    price: Monetary
    is_available: bool
    model_config = ConfigDict(from_attributes=True)

class OptionGroupResponse(BaseModel):
    id: int
    name: str
    min_selection: int
    max_selection: int
    options: List[OptionResponse]
    model_config = ConfigDict(from_attributes=True)

class ProductSimpleResponse(BaseModel):
    id: int
    name: str
    price: Monetary
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Monetary
    image_url: Optional[str] = None
    is_available: bool
    track_stock: bool
    stock_quantity: int
    station: str = "kitchen"
    tags: List[str] = []
    short_code: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    external_id: Optional[str] = None
    option_groups: List[OptionGroupResponse] = []
    recommendations: List[ProductSimpleResponse] = []
    model_config = ConfigDict(from_attributes=True)

class CategoryResponse(BaseModel):
    id: int
    name: str
    products: List[ProductResponse]
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    model_config = ConfigDict(from_attributes=True)

class CategoryCreate(BaseModel):
    name: str = Field(..., example="Lanches")
    order_index: int = 0
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    order_index: Optional[int] = None
    availability_days: Optional[List[int]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class ProductCreate(BaseModel):
    category_id: int = Field(..., example=1)
    name: str = Field(..., example="X-Bacon")
    description: Optional[str] = Field(None, example="Pão, carne, queijo e bacon crocante")
    price: Monetary = Field(..., example=2590)
    image_url: Optional[str] = None
    is_available: bool = True
    track_stock: bool = False
    stock_quantity: int = 0
    station: str = "kitchen"
    tags: List[str] = []
    short_code: Optional[str] = None
    ncm: str = "21069090"
    cfop: str = "5102"
    external_id: Optional[str] = None
    recommended_ids: List[int] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: OptionalMonetary = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    track_stock: Optional[bool] = None
    stock_quantity: Optional[int] = None
    station: Optional[str] = None
    tags: Optional[List[str]] = None
    short_code: Optional[str] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    external_id: Optional[str] = None
    recommended_ids: Optional[List[int]] = None

class OptionGroupCreate(BaseModel):
    name: str = Field(..., example="Escolha o Ponto")
    min_selection: int = 0
    max_selection: int = 1

class OptionCreate(BaseModel):
    name: str = Field(..., example="Bem Passado")
    price: Monetary = 0

class MenuResponse(BaseModel):
    company: CompanyPublic
    categories: List[CategoryResponse]
    model_config = ConfigDict(from_attributes=True)