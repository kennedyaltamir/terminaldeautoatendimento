# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 23:30:00
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import time, datetime
from app.schemas.core import OptionalMonetary

class CompanyPublic(BaseModel):
    name: str
    slug: str
    is_active: bool
    logo_url: Optional[str] = None
    primary_color: str = "#ea580c"
    banner_url: Optional[str] = None
    segment: str = "gastro"
    model_config = ConfigDict(from_attributes=True)

class CompanyAdminSettings(CompanyPublic):
    owner_email: str
    plan_tier: str
    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    # Campos Fiscais (Serão mascarados no router)
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None
    # Pagamentos
    payment_provider: str
    mp_access_token: Optional[str] = None
    service_fee_percentage: OptionalMonetary = 10.0
    fixed_delivery_fee: OptionalMonetary = 0.0
    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    primary_color: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None
    mp_access_token: Optional[str] = None
    service_fee_percentage: OptionalMonetary = None
    fixed_delivery_fee: OptionalMonetary = None
