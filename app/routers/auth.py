
"""
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 5.4.0 (Diamond Hardened Master)
 * DNA_ID: MF-ROUTER-AUTH-V5-4
 * OBJETIVO: Router de Autenticação com Nulidade Protegida e Tipagem Estrita.
 * 
 * CORREÇÕES APLICADAS:
 * 1. Resolvido reportOptionalMemberAccess: request.client agora é validado antes do acesso ao host.
 * 2. Resolvido reportArgumentType: Conversões explícitas para int/str em chamadas de segurança.
 * 3. Resolvido reportGeneralTypeIssues: Avaliação de colunas booleanas via bool().
 */
//
"""

import os
import uuid
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Union, Any, Dict, cast
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db, set_tenant
from app.models import Company, Employee, UserDevice, UserRefreshToken, Table
from app.core import security
from app.core.config import settings
from app.schemas import SignUpRequest, DeviceRegister
from app.services.token_service import token_service

router = APIRouter()
logger = logging.getLogger("AuthRouter")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800
    company_slug: Optional[str] = None
    company_name: Optional[str] = None
    user_role: str
    user_name: str

class RefreshRequest(BaseModel):
    refresh_token: str

class ImpersonateRequest(BaseModel):
    target_email: str

def _get_client_ip(request: Request) -> str:
    if request.client and request.client.host:
        return str(request.client.host)
    return "127.0.0.1"

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> Union[Employee, Company]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="AUTHENTICATION_REQUIRED")
    
    token = auth_header.split(" ")[1]
    try:
        payload = security.decode_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(401, "INVALID_TOKEN_TYPE")
        
        jti = cast(str, payload.get("jti"))
        if token_service.is_revoked(jti):
            raise HTTPException(401, "TOKEN_REVOKED")
        
        company_id = payload.get("company_id")
        if company_id:
            set_tenant(db, str(company_id))
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "INVALID_PAYLOAD")

        user = db.query(Employee).filter(Employee.id == int(user_id)).first()
        if not user or not bool(user.is_active):
            raise HTTPException(401, "USER_NOT_FOUND_OR_INACTIVE")
            
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"INVALID_SESSION: {str(e)}")

@router.post("/token", response_model=TokenResponse)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    client_ip = _get_client_ip(request)
    
    user = db.query(Employee).filter(Employee.email == form_data.username).first()
    
    if not user:
        company = db.query(Company).filter(Company.owner_email == form_data.username).first()
        if company and security.verify_password(form_data.password, str(company.password_hash)):
            user = db.query(Employee).filter(Employee.email == company.owner_email).first()

    if not user or not security.verify_password(form_data.password, str(user.password_hash)):
        security.log_security_event("LOGIN_FAIL", False, {"user": form_data.username, "ip": client_ip})
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")

    if not bool(user.is_active):
        raise HTTPException(status_code=400, detail="ACCOUNT_INACTIVE")

    scope = "admin" if user.role in ["owner", "manager", "admin"] else "user"
    token_data = {
        "sub": str(user.id), 
        "role": str(user.role), 
        "company_id": str(user.company_id),
        "scope": scope
    }
    
    access = security.create_token(token_data, timedelta(minutes=30), "access")
    refresh = security.create_token({"sub": str(user.id)}, timedelta(days=7), "refresh")
    
    db_refresh = UserRefreshToken(
        user_id=int(user.id),
        jti=security.extract_token_jti(refresh),
        token_hash=hashlib.sha256(refresh.encode()).hexdigest(),
        ip_address=client_ip,
        user_agent=request.headers.get("user-agent"),
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(db_refresh)
    db.commit()

    company_info = db.query(Company).filter(Company.id == user.company_id).first()
    
    security.log_security_event("LOGIN_SUCCESS", True, {"user": user.email, "jti": db_refresh.jti})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user_role": str(user.role),
        "user_name": str(user.name),
        "company_slug": str(company_info.slug) if company_info else None,
        "company_name": str(company_info.name) if company_info else None
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_session(request: Request, req: RefreshRequest, db: Session = Depends(get_db)):
    client_ip = _get_client_ip(request)
    try:
        payload = security.decode_token(req.refresh_token)
        jti = cast(str, payload.get("jti"))
        token_hash = hashlib.sha256(req.refresh_token.encode()).hexdigest()
        
        db_token = db.query(UserRefreshToken).filter(
            UserRefreshToken.jti == jti,
            UserRefreshToken.token_hash == token_hash,
            UserRefreshToken.revoked == False
        ).first()
        
        if not db_token or db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            security.log_security_event("REFRESH_DENIED", False, {"jti": jti, "ip": client_ip})
            raise HTTPException(401, "REFRESH_TOKEN_INVALID")

        db_token.revoked = cast(Any, True)
        user = db.query(Employee).filter(Employee.id == db_token.user_id).first()
        
        if not user: raise HTTPException(401, "USER_NOT_FOUND")

        token_data = {"sub": str(user.id), "role": str(user.role), "company_id": str(user.company_id)}
        new_access = security.create_token(token_data, timedelta(minutes=30), "access")
        new_refresh = security.create_token({"sub": str(user.id)}, timedelta(days=7), "refresh")
        
        new_db_token = UserRefreshToken(
            user_id=int(user.id),
            jti=security.extract_token_jti(new_refresh),
            token_hash=hashlib.sha256(new_refresh.encode()).hexdigest(),
            ip_address=client_ip,
            user_agent=request.headers.get("user-agent"),
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(new_db_token)
        db.commit()
        
        company_info = db.query(Company).filter(Company.id == user.company_id).first()
        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "user_role": str(user.role),
            "user_name": str(user.name),
            "company_slug": str(company_info.slug) if company_info else None,
            "company_name": str(company_info.name) if company_info else None
        }
    except Exception:
        raise HTTPException(401, "SESSION_EXPIRED")

@router.post("/register", status_code=201)
def register_company(data: SignUpRequest, db: Session = Depends(get_db)):
    if db.query(Company).filter(Company.owner_email == data.owner_email).first():
        raise HTTPException(400, "EMAIL_ALREADY_EXISTS")

    try:
        password_hash = security.get_password_hash(data.password)
        
        new_company = Company(
            name=data.company_name, 
            slug=data.company_slug, 
            owner_email=data.owner_email,
            password_hash=password_hash, 
            segment=data.segment
        )
        db.add(new_company)
        db.flush() 
        
        owner_employee = Employee(
            company_id=new_company.id,
            name=data.company_name + " Admin",
            email=data.owner_email,
            password_hash=password_hash,
            role="owner",
            is_active=True
        )
        db.add(owner_employee)
        
        set_tenant(db, str(new_company.id))
        db.add(Table(
            company_id=new_company.id, 
            table_number=1, 
            qr_token=hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        ))
        
        db.commit()
        return {"status": "REGISTERED", "slug": new_company.slug}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erro no onboarding: {str(e)}")

@router.post("/impersonate", response_model=TokenResponse)
async def impersonate_user(request: Request, data: ImpersonateRequest, x_super_secret: str = Header(...), db: Session = Depends(get_db)):
    if x_super_secret != settings.SUPER_ADMIN_SECRET:
        security.log_security_event("IMPERSONATION_ATTEMPT_FAIL", False, {"target": data.target_email, "ip": _get_client_ip(request)})
        raise HTTPException(status_code=401, detail="NOT_AUTHORIZED")

    company = db.query(Company).filter(Company.owner_email == data.target_email).first()
    if not company:
        raise HTTPException(status_code=404, detail="TENANT_NOT_FOUND")

    user = db.query(Employee).filter(Employee.email == company.owner_email).first()
    token_data = {
        "sub": str(user.id),
        "role": str(user.role),
        "company_id": str(company.id),
        "impersonator": True 
    }

    access = security.create_token(token_data, timedelta(minutes=15), "access", scope="forensic")
    refresh = security.create_token({"sub": str(user.id)}, timedelta(minutes=30), "refresh")

    security.log_security_event("IMPERSONATION_ACTIVE", True, {"target": data.target_email, "ip": _get_client_ip(request)})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user_role": str(user.role),
        "user_name": f"[SUPPORT] {user.name}",
        "company_slug": str(company.slug),
        "company_name": str(company.name)
    }

@router.post("/logout")
def logout(request: Request, token_data: Any = Depends(security.bearer_scheme)):
    if token_data:
        payload = security.decode_token(token_data.credentials)
        jti = cast(str, payload.get("jti"))
        exp = cast(float, payload.get("exp"))
        remaining = int(exp - datetime.now(timezone.utc).timestamp())
        if remaining > 0:
            token_service.revoke_token(jti, remaining)
            
    security.log_security_event("LOGOUT", True, {"ip": _get_client_ip(request)})
    return {"status": "LOGGED_OUT"}

@router.post("/device")
def register_device(data: DeviceRegister, db: Session = Depends(get_db), current_user: Employee = Depends(get_current_user)):
    device = db.query(UserDevice).filter(UserDevice.fcm_token == data.fcm_token).first()
    if device:
        device.employee_id = cast(Any, current_user.id)
        device.updated_at = cast(Any, datetime.now(timezone.utc))
    else:
        new_device = UserDevice(
            company_id=current_user.company_id,
            employee_id=current_user.id,
            fcm_token=data.fcm_token,
            platform=data.platform,
            device_name=data.device_name
        )
        db.add(new_device)
    db.commit()
    return {"status": "DEVICE_SYNCED"}