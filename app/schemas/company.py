# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-16 13:15:00
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any
from datetime import time, datetime
from app.schemas.core import Monetary, OptionalMonetary

class CompanyPublic(BaseModel):
    name: str
    slug: str
    is_active: bool
    logo_url: Optional[str] = None
    primary_color: str = "#ea580c"
    banner_url: Optional[str] = None
    background_color: Optional[str] = "#f9fafb"
    text_color: Optional[str] = "#111827"
    accent_color: Optional[str] = "#ea580c"
    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    owner_email: Optional[str] = None
    pix_key: Optional[str] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    segment: str = "gastro"
    model_config = ConfigDict(from_attributes=True)

class CompanyAdminSettings(CompanyPublic):
    mp_access_token: Optional[str] = None
    payment_provider: str = "NONE"
    marketplace_fee_percentage: OptionalMonetary = 0
    loyalty_percentage: OptionalMonetary = 0
    plan_tier: str = "free"
    trial_ends_at: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    subscription_status: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None
    service_fee_percentage: OptionalMonetary = 10.0
    fixed_delivery_fee: OptionalMonetary = 0.0
    whatsapp_api_url: Optional[str] = None
    whatsapp_instance: Optional[str] = None
    whatsapp_token: Optional[str] = None
    ifood_merchant_id: Optional[str] = None
    # Kiosk Settings
    kiosk_password_set: bool = False # Retorna true se houver senha configurada, sem retornar o hash
    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    primary_color: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    accent_color: Optional[str] = None
    opens_at: Optional[time] = None
    closes_at: Optional[time] = None
    pix_key: Optional[str] = None
    mp_access_token: Optional[str] = None
    loyalty_percentage: OptionalMonetary = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    whatsapp_api_url: Optional[str] = None
    whatsapp_instance: Optional[str] = None
    whatsapp_token: Optional[str] = None
    wifi_ssid: Optional[str] = None
    wifi_password: Optional[str] = None
    cnpj: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    fiscal_token: Optional[str] = None
    csc_token: Optional[str] = None
    csc_id: Optional[str] = None
    service_fee_percentage: OptionalMonetary = None
    fixed_delivery_fee: OptionalMonetary = None
    ifood_merchant_id: Optional[str] = None
    ifood_token: Optional[str] = None
    # Kiosk Update
    kiosk_password: Optional[str] = None # Plain text para update

class KioskValidationRequest(BaseModel):
    password: str

