"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.2.1 (Update Protocol Restored)
 * DNA_ID: MF-ROUTER-EMPLOYEES-V1-2-1
 * OBJETIVO: Gestão de equipe com suporte a Edição (PATCH) e Reset de Senha.
 */
 """
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from app.database import get_db, set_tenant
from app.models import Company, Employee
from app.schemas.staff import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.routers.auth import get_current_user
from app.core.security import get_password_hash

logger = logging.getLogger("EmployeeRouter")
router = APIRouter()

def require_admin(current_user: any = Depends(get_current_user)):
    role_str = str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role).lower().strip()
    if role_str in ["owner", "manager", "admin"]:
        return current_user
    raise HTTPException(status_code=403, detail="Acesso restrito a administradores.")

@router.get("", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db), current_user: any = Depends(require_admin)):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return db.query(Employee).filter(Employee.company_id == company_id).all()

@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    existing = db.query(Employee).filter(Employee.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Este e-mail já está em uso.")

    new_employee = Employee(
        company_id=company_id,
        name=data.name,
        email=data.email,
        password_hash=get_password_hash(data.password),
        role=data.role,
        is_active=True
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    """
    🛡️ RITO DE ATUALIZAÇÃO SOBERANA
    Permite alterar dados e redefinir senhas com isolamento de tenant.
    """
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    employee = db.query(Employee).filter(
        Employee.id == employee_id, 
        Employee.company_id == company_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado.")

    update_data = data.model_dump(exclude_unset=True)

    # 🔐 Se houver uma nova senha no payload, aplica o hashing Bcrypt
    if "password" in update_data:
        new_password = update_data.pop("password")
        if new_password:
            employee.password_hash = get_password_hash(new_password)
            logger.info(f"Senha do funcionário {employee_id} redefinida pelo admin.")

    # Aplica os demais campos dinamicamente
    for key, value in update_data.items():
        setattr(employee, key, value)

    try:
        db.commit()
        db.refresh(employee)
        return employee
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar colaborador: {e}")
        raise HTTPException(status_code=400, detail="Falha na atualização dos dados.")

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.company_id == company_id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado.")
    
    db.delete(employee)
    db.commit()
    return None