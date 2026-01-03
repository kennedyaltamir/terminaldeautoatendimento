from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Company, Employee, UserRole
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.routers.auth import get_current_user
from app.core.security import get_password_hash

router = APIRouter()

def require_admin(current_user: any = Depends(get_current_user)):
    # Verifica se é um objeto Company (Dono) ou Employee com cargo de gerente
    if isinstance(current_user, Company):
        return current_user
    
    if isinstance(current_user, Employee) and current_user.role in [UserRole.OWNER, UserRole.MANAGER]:
        return current_user
        
    raise HTTPException(status_code=403, detail="Acesso restrito a administradores")

@router.get("", response_model=List[EmployeeResponse])
def get_employees(
    role: str = None,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    # Se for Company, usa o ID dela. Se for Employee, usa o company_id dele.
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    query = db.query(Employee).filter(Employee.company_id == company_id)
    
    if role:
        query = query.filter(Employee.role == role)
        
    return query.all()

@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id

    # Verificar se email já existe
    if db.query(Employee).filter(Employee.email == data.email).first() or \
       db.query(Company).filter(Company.owner_email == data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_employee = Employee(
        company_id=company_id,
        name=data.name,
        email=data.email,
        password_hash=get_password_hash(data.password),
        role=data.role
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.company_id == company_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    db.delete(employee)
    db.commit()
    return None