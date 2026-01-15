
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 01:45:00

from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

# --- AUDIT SCHEMAS ---

class AuditLogResponse(BaseModel):
    id: int
    user_name: Optional[str] = "Sistema"
    user_role: Optional[str] = None
    action: str
    resource: str
    resource_id: Optional[str] = None
    details: Optional[Any] = None
    ip_address: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- FEATURE FLAG SCHEMAS ---

class FeatureFlagUpdate(BaseModel):
    key: str
    is_enabled: bool

class FeatureFlagResponse(BaseModel):
    key: str
    is_enabled: bool
    model_config = ConfigDict(from_attributes=True)

