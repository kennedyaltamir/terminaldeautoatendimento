from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company
from app.schemas import CompanyAdminSettings, CompanyUpdate, PasswordUpdate
from app.routers.auth import get_current_user
from app.core.security import verify_password, get_password_hash

router = APIRouter()

@router.get("/me", response_model=CompanyAdminSettings)
def get_my_company(current_user: Company = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=CompanyAdminSettings)
def update_my_company(
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
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
    current_user: Company = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha atual está incorreta"
        )
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Senha alterada com sucesso"}