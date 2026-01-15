
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 02:20:00

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.core import Monetary, OptionalMonetary

class PromotionBase(BaseModel):
    name: str
    code: Optional[str] = None
    discount_type: str = "percentage"  # percentage, fixed, shipping
    discount_value: Monetary
    min_order_value: Monetary = 0
    max_discount_value: OptionalMonetary = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    is_active: bool = True

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: OptionalMonetary = None
    min_order_value: OptionalMonetary = None
    max_discount_value: OptionalMonetary = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    usage_limit: Optional[int] = None
    is_active: Optional[bool] = None

class PromotionResponse(PromotionBase):
    id: UUID
    company_id: UUID
    current_usage: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

