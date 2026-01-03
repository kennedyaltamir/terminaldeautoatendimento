
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import get_db
from app.models import Company, Employee
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from app.schemas import Token, SignUpRequest
from app.core.limiter import limiter
from datetime import timedelta, datetime

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Tenta Company
    company = db.query(Company).filter(Company.owner_email == form_data.username).first()
    if company and verify_password(form_data.password, company.password_hash):
        access_token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
        return {"access_token": access_token, "refresh_token": "dummy", "token_type": "bearer", "company_slug": company.slug, "company_name": company.name, "user_role": "owner", "user_name": "Admin"}

    # Tenta Employee
    employee = db.query(Employee).filter(Employee.email == form_data.username).first()
    if employee and verify_password(form_data.password, employee.password_hash):
        if not employee.is_active: raise HTTPException(400, "Inativo")
        company = db.query(Company).filter(Company.id == employee.company_id).first()
        access_token = create_access_token(data={"sub": employee.email, "role": employee.role, "account_type": "employee", "company_id": str(company.id)})
        return {"access_token": access_token, "refresh_token": "dummy", "token_type": "bearer", "company_slug": company.slug, "company_name": company.name, "user_role": employee.role, "user_name": employee.name}

    raise HTTPException(status_code=401, detail="Credenciais inválidas")

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
    
    token = create_access_token(data={"sub": new_company.owner_email, "role": "owner", "account_type": "company"})
    return {"access_token": token, "refresh_token": "dummy", "token_type": "bearer", "company_slug": new_company.slug, "company_name": new_company.name, "user_role": "owner", "user_name": "Admin"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_type: str = payload.get("account_type")
        if email is None: raise HTTPException(401, "Token inválido")
    except JWTError:
        raise HTTPException(401, "Token inválido")
        
    if user_type == "company":
        user = db.query(Company).filter(Company.owner_email == email).first()
        if user: 
            user.role = "owner" # Injeta atributo dinâmico
            return user
            
    elif user_type == "employee":
        user = db.query(Employee).filter(Employee.email == email).first()
        if user:
            company = db.query(Company).filter(Company.id == user.company_id).first()
            user.company = company
            user.slug = company.slug
            return user

    raise HTTPException(401, "Usuário não encontrado")
