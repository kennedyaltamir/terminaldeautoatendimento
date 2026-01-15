
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 02:15:00

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.schemas.core import Monetary

class WalletResponse(BaseModel):
    balance: Monetary
    loyalty_percentage: Monetary

class TipReportItem(BaseModel):
    employee_name: str
    total_tips: float
    order_count: int

class DriverLedgerResponse(BaseModel):
    id: int
    type: str
    amount: Monetary
    description: Optional[str] = None
    created_at: datetime
    order_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)

class DriverBalanceResponse(BaseModel):
    driver_id: int
    driver_name: str
    current_debt: Monetary
    transactions: List[DriverLedgerResponse]
    model_config = ConfigDict(from_attributes=True)

class SettleDebtRequest(BaseModel):
    amount: Monetary = Field(..., example=5000)
    description: Optional[str] = "Acerto de contas"

class CouponValidationRequest(BaseModel):
    code: str = Field(..., example="VERAO10")
    total_amount: Monetary = Field(..., example=10000)

class CouponValidationResponse(BaseModel):
    valid: bool
    discount_amount: Monetary
    final_total: Monetary
    message: str
    promotion_id: Optional[UUID] = None

class WebhookCreate(BaseModel):
    target_url: str
    events: List[str]
    secret: Optional[str] = None

class WebhookResponse(BaseModel):
    id: int
    target_url: str
    events: List[str]
    secret: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StripeCheckoutResponse(BaseModel):
    url: str

class FiscalEmissionResponse(BaseModel):
    status: str
    message: str
    nfe_url: Optional[str] = None

