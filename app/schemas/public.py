
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any
from datetime import datetime
from app.schemas.core import Monetary

class CheckTableRequest(BaseModel):
    table_id: int
    qr_token: str
    session_token: Optional[str] = None

class CheckTableResponse(BaseModel):
    status: str
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
    total_spent: Monetary = 0
    access_pin: str

class JoinTableRequest(BaseModel):
    table_id: int
    qr_token: str
    customer_name: str
    pin: Optional[str] = None

class SessionUpdate(BaseModel):
    customer_name: str

class TableSessionDetail(BaseModel):
    id: int
    customer_name: str
    total_spent: Monetary
    start_time: datetime
    orders: List[Any]
    
class TableTransferRequest(BaseModel):
    from_table_id: int
    to_table_id: int
    merge: bool = False

class LeadCreate(BaseModel):
    email: EmailStr
    source: str = "landing_page"

class LeadResponse(BaseModel):
    message: str
    download_url: str

