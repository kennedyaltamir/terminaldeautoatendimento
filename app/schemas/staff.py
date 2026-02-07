# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 12:52:00
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "cashier"
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=4)

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    updated_at: Optional[datetime] = None # 🛡️ FIX: Recebe timestamp para check de concorrência

class EmployeeResponse(EmployeeBase):
    id: int
    company_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None # 🛡️ FIX: Expõe versão atual
    
    model_config = ConfigDict(from_attributes=True)
