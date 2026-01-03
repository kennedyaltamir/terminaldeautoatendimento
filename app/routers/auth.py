from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import get_db
from app.models import Company, PlanTier, Employee, UserRole
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.schemas import Token, TokenData, SignUpRequest
from datetime import timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Tentar login como DONO (Company)
    company = db.query(Company).filter(Company.owner_email == form_data.username).first()
    
    if company and verify_password(form_data.password, company.password_hash):
        # CORREÇÃO: Usando 'account_type' em vez de 'type' para evitar sobrescrita
        access_token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
        refresh_token = create_refresh_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
        
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer",
            "company_slug": company.slug,
            "company_name": company.name,
            "user_role": "owner",
            "user_name": "Admin"
        }

    # 2. Tentar login como FUNCIONÁRIO
    employee = db.query(Employee).filter(Employee.email == form_data.username).first()
    
    if employee and verify_password(form_data.password, employee.password_hash):
        if not employee.is_active:
            raise HTTPException(status_code=400, detail="Usuário inativo.")
            
        # Carregar empresa para pegar o slug
        company = db.query(Company).filter(Company.id == employee.company_id).first()
        
        # CORREÇÃO: Usando 'account_type'
        access_token = create_access_token(data={"sub": employee.email, "role": employee.role, "account_type": "employee", "company_id": str(company.id)})
        refresh_token = create_refresh_token(data={"sub": employee.email, "role": employee.role, "account_type": "employee"})
        
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token, 
            "token_type": "bearer",
            "company_slug": company.slug,
            "company_name": company.name,
            "user_role": employee.role,
            "user_name": employee.name
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorretos",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        # CORREÇÃO: Lendo 'account_type'
        user_type: str = payload.get("account_type")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    if user_type == "company":
        user = db.query(Company).filter(Company.owner_email == email).first()
        if user:
            user.role = "owner"
            return user
            
    elif user_type == "employee":
        user = db.query(Employee).filter(Employee.email == email).first()
        if user:
            user.company = db.query(Company).filter(Company.id == user.company_id).first()
            user.slug = user.company.slug
            user.id = user.company.id # Hack para compatibilidade
            return user

    raise credentials_exception

@router.post("/register", response_model=Token, status_code=201)
def register_company(data: SignUpRequest, db: Session = Depends(get_db)):
    if db.query(Company).filter(Company.owner_email == data.owner_email).first():
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")
    
    if db.query(Employee).filter(Employee.email == data.owner_email).first():
        raise HTTPException(status_code=400, detail="Este email já está em uso por um funcionário.")
    
    if db.query(Company).filter(Company.slug == data.company_slug).first():
        raise HTTPException(status_code=400, detail="Este link (slug) já está em uso. Escolha outro.")

    new_company = Company(
        name=data.company_name,
        slug=data.company_slug,
        owner_email=data.owner_email,
        password_hash=get_password_hash(data.password),
        plan_tier=PlanTier.FREE,
        primary_color="#ea580c"
    )
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    # CORREÇÃO: Usando 'account_type'
    access_token = create_access_token(data={"sub": new_company.owner_email, "role": "owner", "account_type": "company"})
    refresh_token = create_refresh_token(data={"sub": new_company.owner_email, "role": "owner", "account_type": "company"})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer",
        "company_slug": new_company.slug,
        "company_name": new_company.name,
        "user_role": "owner",
        "user_name": "Admin"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Header(..., alias="X-Refresh-Token"), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        # Simplificação: Apenas revalida companies por enquanto
        company = db.query(Company).filter(Company.owner_email == email).first()
        if not company:
             raise credentials_exception
            
        # CORREÇÃO: Usando 'account_type'
        new_access_token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company"})
        new_refresh_token = create_refresh_token(data={"sub": email, "role": "owner", "account_type": "company"})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "company_slug": company.slug,
            "company_name": company.name,
            "user_role": "owner",
            "user_name": "Admin"
        }
        
    except JWTError:
        raise credentials_exception