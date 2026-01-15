
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 01:45:00

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "cashier"  # kitchen, cashier, manager, driver
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=4)

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    company_id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

