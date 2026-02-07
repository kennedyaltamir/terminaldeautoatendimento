# DOMAIN: BACKEND / SCHEMAS
# LAST_MODIFIED: 2026-02-05 07:25:00
"""
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 13.5.0
 * DNA_ID: MF-SCHEMAS-ORDERS-V13-5
 * OBJETIVO: Contrato Universal de Dados para Pedidos, Itens e Mesas.
 * Comportamento esperado: 
 *  1. Provê blindagem total contra valores NULL no banco (Null-Resilience).
 *  2. Gerencia entradas e saídas de dados para KDS, PDV e Logística GPS.
 *  3. Garante validade de payloads financeiros usando o tipo Monetary.
 */
//
"""
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional, Any, Union
from uuid import UUID
from datetime import datetime
from app.schemas.core import Monetary, OptionalMonetary
from app.schemas.menu import ProductResponse
import re

# ==============================================================================
# 📦 DOMAIN: ORDER ITEMS (COMPOSIÇÃO)
# ==============================================================================
class OrderItemOptionResponse(BaseModel):
    name: str
    price: Monetary
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    unit_price: Monetary
    notes: Optional[str] = None
    product: ProductResponse
    selected_options: List[OrderItemOptionResponse] = []
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, example=1)
    notes: Optional[str] = None
    selected_options: List[int] = []

# ==============================================================================
# 🪑 DOMAIN: TABLES & SERVICE (INFRAESTRUTURA)
# ==============================================================================
class TableSimpleResponse(BaseModel):
    table_number: int
    model_config = ConfigDict(from_attributes=True)

class TableCreate(BaseModel):
    table_number: int

class TableBulkCreate(BaseModel):
    start: int
    end: int

class TablePositionUpdate(BaseModel):
    id: int
    x: float
    y: float

class TableResponse(BaseModel):
    id: int
    table_number: int
    qr_token: str
    is_active: bool = True
    position_x: Optional[float] = 0.0
    position_y: Optional[float] = 0.0
    capacity: int = 4
    model_config = ConfigDict(from_attributes=True)

class TableDashboardResponse(TableResponse):
    status: str 
    active_session: Optional[Any] = None
    service_request: Optional[str] = None

class TableTransferRequest(BaseModel):
    from_table_id: int
    to_table_id: int
    merge: bool = False

class OpenTableRequest(BaseModel):
    customer_name: str

class CloseTableRequest(BaseModel):
    payment_method: str
    custom_service_fee: Optional[float] = None

class SessionUpdate(BaseModel):
    customer_name: Optional[str] = None
    is_active: Optional[bool] = None

# ==============================================================================
# 📋 DOMAIN: ORDERS (ENTIDADE PRINCIPAL)
# ==============================================================================
class OrderResponse(BaseModel):
    """
    Schema de Saída Resiliente.
    Garante que a API não crash com 'Internal Server Error' se o banco tiver nulos.
    """
    id: UUID
    status: str
    order_type: str
    origin: str
    customer_name: Optional[str] = "Cliente"
    customer_phone: Optional[str] = None
    
    # 🛰️ GPS & Logistics
    delivery_address: Optional[str] = None
    delivery_lat: Optional[float] = None
    delivery_lng: Optional[float] = None
    delivery_code: Optional[str] = None
    pickup_note: Optional[str] = None
    
    # 💰 Financial Data (Null-Safe)
    subtotal: OptionalMonetary = None
    discount_amount: OptionalMonetary = 0
    cashback_earned: OptionalMonetary = 0
    service_fee: OptionalMonetary = 0
    delivery_fee: OptionalMonetary = 0
    total_amount: Monetary
    payment_method: Optional[str] = "cash"
    payment_status: Optional[str] = "pending"
    
    # Integrations
    external_order_id: Optional[str] = None
    mp_qr_code: Optional[str] = None
    mp_qr_code_base64: Optional[str] = None
    driver_id: Optional[int] = None
    
    # Status & Metadata
    fiscal_status: Optional[str] = "pending"
    nfe_url_pdf: Optional[str] = None
    created_at: datetime
    finished_at: Optional[datetime] = None
    
    # Relationships
    table: Optional[TableSimpleResponse] = None
    items: List[OrderItemResponse] = []
    feedback: Optional[Any] = None
    model_config = ConfigDict(from_attributes=True)

class TableSessionDetail(BaseModel):
    id: int
    customer_name: str
    is_active: bool
    created_at: datetime
    closed_at: Optional[datetime] = None
    orders: List[OrderResponse] = []
    total_spent: Monetary
    access_pin: str
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    """Contrato de Criação de Pedidos (Omnichannel)."""
    table_id: Optional[int] = None
    qr_token: Optional[str] = None
    order_type: str = Field(default="dine_in", pattern="^(dine_in|delivery|takeout|on_site)$")
    origin: str = Field(default="mesaflow", pattern="^(mesaflow|kiosk|mobile|waiter|admin|ifood|rappi)$")
    customer_name: str = Field(..., min_length=2)
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    pickup_note: Optional[str] = None
    payment_method: str = Field(default="cash", pattern="^(pix|card|cash|online)$")
    items: List[OrderItemCreate]
    use_balance: bool = False
    coupon_code: Optional[str] = None

    @field_validator('customer_phone')
    @classmethod
    def validate_phone(cls, v):
        if not v: return v
        clean = re.sub(r'\D', '', v)
        return clean if len(clean) >= 8 else v

# ==============================================================================
# 🛠️ DOMAIN: SYSTEM & TASKS
# ==============================================================================
class OrderPagination(BaseModel):
    data: List[OrderResponse]
    total: int
    page: int
    limit: int

class FeedbackCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    score: int
    comment: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DispatchOrderRequest(BaseModel):
    driver_id: Optional[int] = None

class CompleteDeliveryRequest(BaseModel):
    code: Optional[str] = None

class ServiceRequestResponse(BaseModel):
    id: int
    table_number: int
    service_type: str 
    notes: Optional[str] = None
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)