from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company, Employee, UserRole
from app.schemas import CompanyAdminSettings, CompanyUpdate, PasswordUpdate
from app.routers.auth import get_current_user
from app.core.security import verify_password, get_password_hash

router = APIRouter()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    raise HTTPException(status_code=403, detail="Apenas o dono pode alterar configurações")

@router.get("/me", response_model=CompanyAdminSettings)
def get_my_company(current_user: any = Depends(get_current_user)):
    # Todos podem ver dados básicos (nome, logo), mas dados sensíveis devem ser filtrados no frontend ou aqui
    # Por simplicidade, retornamos o objeto, mas o frontend do garçom não tem acesso à tela de config.
    if isinstance(current_user, Employee):
        return current_user.company
    return current_user

@router.patch("/me", response_model=CompanyAdminSettings)
def update_my_company(
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner) # Proteção: Apenas Dono
):
    update_data = company_data.model_dump(exclude_unset=True)
    
    if "mp_access_token" in update_data:
        token = update_data["mp_access_token"]
        if token == "":
            update_data["mp_access_token"] = None
        elif token and not token.startswith("APP_USR-"):
            raise HTTPException(status_code=400, detail="Token do Mercado Pago inválido. Deve começar com APP_USR-")

    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.patch("/me/password", status_code=status.HTTP_200_OK)
def update_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    # Permite que funcionários também troquem a própria senha
    if isinstance(current_user, Employee):
        if not verify_password(password_data.current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Senha incorreta")
        current_user.password_hash = get_password_hash(password_data.new_password)
    else:
        if not verify_password(password_data.current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Senha incorreta")
        current_user.password_hash = get_password_hash(password_data.new_password)
        
    db.commit()
    return {"message": "Senha alterada com sucesso"}