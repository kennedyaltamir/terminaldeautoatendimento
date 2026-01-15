
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import re
from app.schemas.core import sanitize_html

class SignUpRequest(BaseModel):
    company_name: str = Field(..., min_length=3, example="Pizzaria do Bairro")
    company_slug: str = Field(..., min_length=3, pattern="^[a-z0-9-]+$", example="pizzaria-bairro")
    owner_email: EmailStr = Field(..., example="contato@pizzaria.com")
    password: str = Field(..., min_length=8, example="SenhaSegura123")
    owner_phone: Optional[str] = Field(None, example="5511999999999")
    owner_role: Optional[str] = Field(None, example="Gerente")
    segment: str = Field("gastro", example="gastro")

    @field_validator('company_name', 'owner_role')
    @classmethod
    def sanitize(cls, v): 
        return sanitize_html(v)

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Za-z]', v) or not re.search(r'[0-9]', v):
            raise ValueError('A senha deve conter letras e números')
        return v

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    company_slug: str
    company_name: str
    user_role: str
    user_name: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class DeviceRegister(BaseModel):
    fcm_token: str = Field(..., example="fcm_token_123")
    device_name: Optional[str] = Field(None, example="Samsung S21")
    platform: Optional[str] = "android"

