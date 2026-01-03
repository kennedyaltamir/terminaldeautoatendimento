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
    if current_user.role not in ["owner", "manager"]:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return current_user

@router.get("", response_model=List[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    # current_user.id aqui é o company_id (devido ao hack no auth.py)
    return db.query(Employee).filter(Employee.company_id == current_user.id).all()

@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    # Verificar se email já existe
    if db.query(Employee).filter(Employee.email == data.email).first() or \
       db.query(Company).filter(Company.owner_email == data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_employee = Employee(
        company_id=current_user.id,
        name=data.name,
        email=data.email,
        password_hash=get_password_hash(data.password),
        role=data.role
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.company_id == current_user.id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
    for key, value in update_data.items():
        setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id,
        Employee.company_id == current_user.id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    db.delete(employee)
    db.commit()
    return None