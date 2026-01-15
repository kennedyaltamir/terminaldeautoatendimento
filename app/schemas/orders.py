# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 09:15:00
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from app.schemas.core import Monetary, OptionalMonetary
from app.schemas.menu import ProductResponse

# --- TABLE SCHEMAS ---
class TableCreate(BaseModel):
    table_number: int

class TableBulkCreate(BaseModel):
    start: int
    end: int

class TablePositionUpdate(BaseModel):
    id: int
    x: float
    y: float

class TableSimpleResponse(BaseModel):
    table_number: int
    model_config = ConfigDict(from_attributes=True)

class TableResponse(BaseModel):
    id: int
    table_number: int
    qr_token: str
    is_active: bool = True 
    position_x: float = 0.0
    position_y: float = 0.0
    model_config = ConfigDict(from_attributes=True)

class OpenTableRequest(BaseModel):
    customer_name: str

class CloseTableRequest(BaseModel):
    payment_method: str
    custom_service_fee: Optional[float] = None

class SessionUpdate(BaseModel):
    customer_name: str

class TableSessionDetail(BaseModel):
    id: int
    customer_name: str
    total_spent: Monetary
    start_time: datetime
    orders: List[Any] 

class TableDashboardResponse(TableResponse):
    status: str
    active_session: Optional[Any] = None
    service_request: Optional[str] = None
    is_active: Optional[bool] = True 

class TableTransferRequest(BaseModel):
    from_table_id: int
    to_table_id: int
    merge: bool = False

# --- ORDER SCHEMAS ---
class OrderItemOptionResponse(BaseModel):
    name: str
    price: Monetary
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(BaseModel):
    id: int
    quantity: int = Field(..., example=1)
    notes: Optional[str] = Field(None, example="Sem cebola")
    product: ProductResponse
    selected_options: List[OrderItemOptionResponse] = []
    model_config = ConfigDict(from_attributes=True)

class FeedbackResponse(BaseModel):
    score: int
    comment: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    status: str
    order_type: str
    origin: str = "mesaflow"
    external_order_id: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_phone: Optional[str] = None
    subtotal: OptionalMonetary = None
    discount_amount: Monetary = 0
    cashback_earned: Monetary = 0
    payment_method: str
    payment_status: str
    total_amount: Monetary
    customer_name: Optional[str] = None
    created_at: datetime
    finished_at: Optional[datetime] = None
    table: Optional[TableSimpleResponse] = None
    items: List[OrderItemResponse] = []
    mp_qr_code: Optional[str] = None
    mp_qr_code_base64: Optional[str] = None
    driver_id: Optional[int] = None
    fiscal_status: str = "pending"
    nfe_url_pdf: Optional[str] = None
    nfe_url_xml: Optional[str] = None
    service_fee: Monetary = 0
    delivery_fee: Monetary = 0
    feedback: Optional[FeedbackResponse] = None
    model_config = ConfigDict(from_attributes=True)

class OrderPagination(BaseModel):
    data: List[OrderResponse]
    total: int
    page: int
    limit: int

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    notes: Optional[str] = None
    selected_options: List[int] = []

class OrderCreate(BaseModel):
    table_id: Optional[int] = None
    qr_token: Optional[str] = None
    order_type: str = "dine_in"
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    customer_name: Optional[str] = "Cliente"
    payment_method: str = "cash"
    use_balance: bool = False
    items: List[OrderItemCreate]
    coupon_code: Optional[str] = None

class DispatchOrderRequest(BaseModel):
    # FIX: driver_id tornado opcional com default None para evitar erro 422 em corpos vazios
    driver_id: Optional[int] = None

class CompleteDeliveryRequest(BaseModel):
    code: Optional[str] = None

class FeedbackCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ServiceRequestResponse(BaseModel):
    id: int
    table_number: int
    service_type: str
    notes: Optional[str] = None
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

