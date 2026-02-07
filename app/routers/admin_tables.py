# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 07:35:00
# DESCRIPTION: Router de Mesas com correção de tipagem para opener_id (UUID vs Int).
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.database import get_db, set_tenant
from app.models import Company, Table, TableSession, Order, OrderItem, Employee
from app.schemas import (
    TableResponse, TableCreate, TableBulkCreate, TableDashboardResponse, 
    OpenTableRequest, CloseTableRequest, TablePositionUpdate, 
    TableTransferRequest
)
from app.routers.auth import get_current_user
from app.websockets import manager
from app.services.table_service import TableService

router = APIRouter()
table_service = TableService()

def get_company_id(user: any) -> str:
    return str(user.id if hasattr(user, 'owner_email') else user.company_id)

@router.get("", response_model=List[TableResponse])
def get_tables(db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    return table_service.get_all_tables(db, company_id)

@router.post("", response_model=TableResponse, status_code=201)
def create_single_table(data: TableCreate, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    return table_service.create_table(db, company_id, data.table_number)

@router.post("/bulk", status_code=201)
def create_bulk_tables(data: TableBulkCreate, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    count = table_service.bulk_create(db, company_id, data.start, data.end)
    return {"message": f"{count} mesas criadas com sucesso."}

@router.patch("/positions", status_code=200)
def update_positions(positions: List[TablePositionUpdate], db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    table_service.update_positions(db, company_id, positions)
    return {"message": "Layout do salão salvo com sucesso."}

@router.get("/dashboard", response_model=List[TableDashboardResponse])
def get_tables_dashboard(db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    return table_service.get_dashboard_data(db, company_id)

@router.post("/transfer", status_code=200)
async def transfer_table(data: TableTransferRequest, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company = current_user if isinstance(current_user, Company) else current_user.company
    set_tenant(db, str(company.id))
    table_service.transfer_or_merge(db, company.id, data.from_table_id, data.to_table_id, data.merge)
    await manager.broadcast({"type": "order_update", "table_id": data.to_table_id}, company.slug)
    return {"message": "Transferência concluída com sucesso."}

@router.post("/{table_id}/open", status_code=200)
async def open_table_session(table_id: int, data: OpenTableRequest, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company = current_user if isinstance(current_user, Company) else current_user.company
    set_tenant(db, str(company.id))
    
    # 🛡️ FIX: Validação de Tipo para opener_id
    # Se o usuário for um Employee (tem ID inteiro), passamos o ID.
    # Se for Company (tem ID UUID), passamos None, pois a tabela espera Integer.
    opener_id = None
    if isinstance(current_user, Employee):
        opener_id = current_user.id
    elif hasattr(current_user, 'id') and isinstance(current_user.id, int):
        opener_id = current_user.id
        
    pin = table_service.open_session(db, table_id, company.id, data.customer_name, opener_id)
    await manager.broadcast({"type": "order_update", "table_id": table_id}, company.slug)
    return {"message": "Mesa aberta", "pin": pin}

@router.post("/{table_id}/close", status_code=200)
async def close_table_session(table_id: int, data: CloseTableRequest, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company = current_user if isinstance(current_user, Company) else current_user.company
    set_tenant(db, str(company.id))
    pix_data = await table_service.close_session(db, table_id, company, data.payment_method, data.custom_service_fee)
    await manager.broadcast({"type": "order_update", "table_id": table_id}, company.slug)
    return {"message": "Mesa fechada", "pix_data": pix_data}

@router.delete("/{table_id}", status_code=204)
def delete_table(table_id: int, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    table_service.delete_table(db, company_id, table_id)
    return None

@router.get("/{table_id}/active-session")
def get_table_active_session(table_id: int, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    company_id = get_company_id(current_user)
    set_tenant(db, company_id)
    session = db.query(TableSession).options(
        selectinload(TableSession.orders).selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(
        TableSession.table_id == table_id,
        TableSession.company_id == company_id,
        TableSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Nenhuma sessão ativa nesta mesa")
        
    # Recalcula total gasto on-the-fly
    total = sum(o.total_amount for o in session.orders if o.payment_status != 'refunded')
    session.total_spent = total
    return session
