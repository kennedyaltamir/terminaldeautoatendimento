# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-09
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import get_db, set_tenant
from app.models import Company, Employee, UserDevice, AuditAction, Table
from app.core.security import (
    verify_password, get_password_hash, create_access_token, 
    create_refresh_token, SECRET_KEY, ALGORITHM
)
from app.services.token_service import token_service
from app.schemas import Token, SignUpRequest, DeviceRegister
from app.services.audit_service import AuditService
from pydantic import BaseModel
from datetime import datetime, timezone
import os
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

class ImpersonateRequest(BaseModel):
    target_email: str

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(oauth2_scheme)):
    """
    Revoga o token atual, adicionando seu JTI à blacklist no Redis.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp = payload.get("exp")

        if jti and exp:
            now = datetime.now(timezone.utc).timestamp()
            remaining = int(exp - now)
            if remaining > 0:
                token_service.revoke_token(jti, remaining)

        return None
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_type: str = payload.get("account_type")
        is_impersonator: bool = payload.get("impersonator", False) 
        company_id: str = payload.get("company_id")
        jti: str = payload.get("jti")

        if email is None: raise HTTPException(401, "Token inválido")

        # SECURITY HARDENING: Verificação de Blacklist
        if token_service.is_revoked(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão encerrada. Por favor, faça login novamente.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # RLS: Configura o contexto do banco de dados
        if company_id:
            set_tenant(db, company_id)

    except JWTError:
        raise HTTPException(401, "Token inválido")

    if user_type == "company":
        user = db.query(Company).filter(Company.owner_email == email).first()
        if user: 
            user.role = "owner"
            user.is_impersonator = is_impersonator 
            return user

    elif user_type == "employee":
        user = db.query(Employee).filter(Employee.email == email).first()
        if user:
            company = db.query(Company).filter(Company.id == user.company_id).first()
            user.company = company
            user.slug = company.slug
            user.is_impersonator = is_impersonator 
            return user

    raise HTTPException(401, "Usuário não encontrado")

@router.post("/impersonate", response_model=Token)
async def impersonate_user(
    request: Request,
    data: ImpersonateRequest,
    x_super_secret: str = Header(...),
    db: Session = Depends(get_db)
):
    master_secret = os.getenv("SUPER_ADMIN_SECRET")
    if not master_secret or x_super_secret != master_secret:
        raise HTTPException(status_code=401, detail="Acesso negado ao modo suporte.")

    company = db.query(Company).filter(Company.owner_email == data.target_email).first()
    if not company:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    token_data = {
        "sub": company.owner_email,
        "role": "owner",
        "account_type": "company",
        "company_id": str(company.id),
        "impersonator": True 
    }

    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)

    AuditService.log(
        db, company, AuditAction.IMPERSONATE, "SupportAccess", str(company.id),
        details={"impersonator_ip": request.client.host, "target": data.target_email},
        request=request
    )

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer", 
        "company_slug": company.slug, 
        "company_name": company.name, 
        "user_role": "owner", 
        "user_name": f"[SUPORTE] {company.name}"
    }

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.owner_email == form_data.username).first()
    if company and verify_password(form_data.password, company.password_hash):
        token_data = {
            "sub": company.owner_email, 
            "role": "owner", 
            "account_type": "company",
            "company_id": str(company.id)
        }
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer", 
            "company_slug": company.slug, 
            "company_name": company.name, 
            "user_role": "owner", 
            "user_name": "Admin"
        }

    employee = db.query(Employee).filter(Employee.email == form_data.username).first()
    if employee and verify_password(form_data.password, employee.password_hash):
        if not employee.is_active: raise HTTPException(400, "Usuário inativo")
        company = db.query(Company).filter(Company.id == employee.company_id).first()
        token_data = {"sub": employee.email, "role": employee.role, "account_type": "employee", "company_id": str(company.id)}

        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer", 
            "company_slug": company.slug, 
            "company_name": company.name, 
            "user_role": employee.role, 
            "user_name": employee.name
        }

    raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(x_refresh_token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(x_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")

        email = payload.get("sub")
        user_type = payload.get("account_type")
        is_impersonated = payload.get("impersonator", False)

        if user_type == "company":
            user = db.query(Company).filter(Company.owner_email == email).first()
            if not user: raise HTTPException(401)
            token_data = {
                "sub": user.owner_email, 
                "role": "owner", 
                "account_type": "company", 
                "company_id": str(user.id),
                "impersonator": is_impersonated
            }
            company_info = {"slug": user.slug, "name": user.name, "role": "owner", "user_name": "Admin"}
        else:
            user = db.query(Employee).filter(Employee.email == email).first()
            if not user or not user.is_active: raise HTTPException(401)
            company = db.query(Company).filter(Company.id == user.company_id).first()
            token_data = {"sub": user.email, "role": user.role, "account_type": "employee", "company_id": str(company.id), "impersonator": is_impersonated}
            company_info = {"slug": company.slug, "name": company.name, "role": user.role, "user_name": user.name}

        return {
            "access_token": create_access_token(data=token_data),
            "refresh_token": create_refresh_token(data=token_data),
            "token_type": "bearer",
            "company_slug": company_info["slug"],
            "company_name": company_info["name"],
            "user_role": company_info["role"],
            "user_name": company_info["user_name"]
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Sessão expirada.")

@router.post("/google", response_model=Token)
async def google_auth(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    token = data.get("credential")
    client_id = os.getenv("GOOGLE_CLIENT_ID")

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)
        email = idinfo['email']
        name = idinfo.get('name', 'Usuário Google')

        company = db.query(Company).filter(Company.owner_email == email).first()
        if not company:
            slug = email.split('@')[0].replace('.', '-') + f"-{os.urandom(2).hex()}"
            company = Company(name=f"Loja de {name.split(' ')[0]}", slug=slug, owner_email=email, password_hash=None, is_email_verified=True)
            db.add(company)
            db.commit()
            db.refresh(company)
            
            # Auto-create first table for Zero-Touch Onboarding
            set_tenant(db, str(company.id))
            table = Table(company_id=company.id, table_number=1, qr_token=str(uuid.uuid4()))
            db.add(table)
            db.commit()

        token_data = {
            "sub": company.owner_email, 
            "role": "owner", 
            "account_type": "company",
            "company_id": str(company.id)
        }
        return {
            "access_token": create_access_token(data=token_data),
            "refresh_token": create_refresh_token(data=token_data),
            "token_type": "bearer",
            "company_slug": company.slug,
            "company_name": company.name, 
            "user_role": "owner",
            "user_name": name
        }
    except Exception:
        raise HTTPException(401, "Autenticação social falhou")

@router.post("/register", response_model=Token, status_code=201)
def register_company(data: SignUpRequest, db: Session = Depends(get_db)):
    if db.query(Company).filter(Company.owner_email == data.owner_email).first():
        raise HTTPException(400, "Email já existe")

    new_company = Company(
        name=data.company_name, slug=data.company_slug, owner_email=data.owner_email,
        password_hash=get_password_hash(data.password), segment=data.segment
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    # Auto-create first table for Zero-Touch Onboarding
    # Precisamos setar o tenant context para o RLS permitir a inserção
    set_tenant(db, str(new_company.id))
    table = Table(company_id=new_company.id, table_number=1, qr_token=str(uuid.uuid4()))
    db.add(table)
    db.commit()

    token_data = {
        "sub": new_company.owner_email, 
        "role": "owner", 
        "account_type": "company",
        "company_id": str(new_company.id)
    }
    return {
        "access_token": create_access_token(data=token_data),
        "refresh_token": create_refresh_token(data=token_data),
        "token_type": "bearer", 
        "company_slug": new_company.slug, 
        "company_name": new_company.name, 
        "user_role": "owner", 
        "user_name": "Admin"
    }

@router.post("/device", status_code=200)
def register_device(
    data: DeviceRegister,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    if not isinstance(current_user, Employee):
        raise HTTPException(status_code=403, detail="Apenas funcionários podem registrar dispositivos móveis.")

    device = db.query(UserDevice).filter(UserDevice.fcm_token == data.fcm_token).first()

    if device:
        device.employee_id = current_user.id
        device.company_id = current_user.company_id
        device.device_name = data.device_name
        device.platform = data.platform
        device.updated_at = datetime.now()
    else:
        device = UserDevice(
            company_id=current_user.company_id,
            employee_id=current_user.id,
            fcm_token=data.fcm_token,
            device_name=data.device_name,
            platform=data.platform
        )
        db.add(device)

    db.commit()
    return {"message": "Dispositivo registrado com sucesso"}

@router.delete("/device/{token}", status_code=204)
def unregister_device(
    token: str,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    device = db.query(UserDevice).filter(UserDevice.fcm_token == token).first()
    if device:
        is_owner = isinstance(current_user, Employee) and device.employee_id == current_user.id
        is_admin = isinstance(current_user, Company) and device.company_id == current_user.id
        if is_owner or is_admin:
            db.delete(device)
            db.commit()
        else:
            raise HTTPException(status_code=403, detail="Sem permissão")
    return None
