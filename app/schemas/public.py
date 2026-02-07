# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Any, Union, TYPE_CHECKING, TypeAlias
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.core import Monetary
else:
    try:
        from app.schemas.core import Monetary
    except:
        Monetary: TypeAlias = Any

class CheckTableRequest(BaseModel):
    """
    Valida o status de uma mesa via QR Code ou Token de Sessão.
    O Pydantic v2 converte automaticamente strings numéricas para int.
    """
    table_id: int = Field(..., description="ID numérico da mesa")
    qr_token: Optional[str] = None
    session_token: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class JoinTableRequest(BaseModel):
    table_id: int
    qr_token: str
    customer_name: str
    pin: Optional[str] = None

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int
    notes: Optional[str] = None
    options: List[int] = []

class CreateOrderRequest(BaseModel):
    table_id: Optional[Union[int, str]] = None
    items: List[OrderItemSchema]
    customer_name: Optional[str] = "Cliente"
    session_token: Optional[str] = None

class LeadCreate(BaseModel):
    email: EmailStr
    source: str = "landing_page"

class CheckTableResponse(BaseModel):
    status: str # 'free', 'active', 'blocked'
    customer_name: Optional[str] = None
    session_token: Optional[str] = None
    access_pin: Optional[str] = None
    requires_pin: bool = False

class TableSessionResponse(BaseModel):
    id: int
    customer_name: str
    is_active: bool
    created_at: datetime
    orders: List[Any] = []
    total_spent: Any = 0 
    access_pin: str

class LeadResponse(BaseModel):
    message: str
    download_url: str