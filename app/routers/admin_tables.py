from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from typing import List
import uuid
from datetime import datetime
from decimal import Decimal
from app.database import get_db
from app.models import Company, Table, TableSession, Order, ServiceRequest, OrderStatus, PaymentStatus, OrderItem, PaymentMethod, Employee, ServiceFeeLedger
from app.schemas import (
    TableResponse, TableCreate, TableBulkCreate, TableDashboardResponse, 
    OpenTableRequest, CloseTableRequest, TablePositionUpdate, SessionUpdate, 
    TableSessionDetail, TableTransferRequest
)
from app.routers.auth import get_current_user
from app.websockets import manager

router = APIRouter()

@router.get("", response_model=List[TableResponse])
def get_tables(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    # Correção: Usar company_id corretamente dependendo do tipo de usuário
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return db.query(Table).filter(Table.company_id == company_id).order_by(Table.table_number).all()

@router.post("", response_model=TableResponse, status_code=201)
def create_table(
    table_data: TableCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    exists = db.query(Table).filter(Table.company_id == company_id, Table.table_number == table_data.table_number).first()
    if exists:
        raise HTTPException(status_code=400, detail=f"Mesa {table_data.table_number} já existe")
    new_table = Table(company_id=company_id, table_number=table_data.table_number, qr_token=uuid.uuid4().hex)
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.post("/bulk", status_code=201)
def create_tables_bulk(
    bulk_data: TableBulkCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    if bulk_data.start > bulk_data.end:
        raise HTTPException(status_code=400, detail="O início deve ser menor que o fim")
    created_count = 0
    for num in range(bulk_data.start, bulk_data.end + 1):
        exists = db.query(Table).filter(Table.company_id == company_id, Table.table_number == num).first()
        if not exists:
            new_table = Table(company_id=company_id, table_number=num, qr_token=uuid.uuid4().hex)
            db.add(new_table)
            created_count += 1
    db.commit()
    return {"message": f"{created_count} mesas criadas"}

@router.delete("/{table_id}", status_code=204)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    table = db.query(Table).filter(Table.id == table_id, Table.company_id == company_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    db.delete(table)
    db.commit()
    return None

@router.get("/dashboard", response_model=List[TableDashboardResponse])
def get_tables_dashboard(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    tables = db.query(Table).filter(Table.company_id == company_id).order_by(Table.table_number).all()
    dashboard_data = []
    for table in tables:
        active_session = db.query(TableSession).filter(TableSession.table_id == table.id, TableSession.is_active == True).first()
        active_request = db.query(ServiceRequest).filter(ServiceRequest.table_id == table.id, ServiceRequest.status == "pending").first()
        status = "free"
        session_summary = None
        if active_session:
            status = "occupied"
            orders = db.query(Order).filter(Order.session_id == active_session.id).all()
            total = sum(o.total_amount for o in orders)
            session_summary = {
                "id": active_session.id,
                "customer_name": active_session.customer_name,
                "total_spent": total,
                "start_time": active_session.created_at
            }
        if active_request:
            status = "alert"
        dashboard_data.append({
            "id": table.id,
            "table_number": table.table_number,
            "qr_token": table.qr_token,
            "status": status,
            "position_x": table.position_x,
            "position_y": table.position_y,
            "active_session": session_summary,
            "service_request": active_request.service_type if active_request else None
        })
    return dashboard_data

@router.post("/{table_id}/open", status_code=200)
def open_table_session(
    table_id: int,
    data: OpenTableRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    table = db.query(Table).filter(Table.id == table_id, Table.company_id == company_id).first()
    if not table: raise HTTPException(404, "Mesa não encontrada")
    existing = db.query(TableSession).filter(TableSession.table_id == table.id, TableSession.is_active == True).first()
    if existing: raise HTTPException(400, "Mesa já está ocupada")
    
    # Identificar quem abriu (para gorjeta)
    opener_id = None
    if isinstance(current_user, Employee):
        opener_id = current_user.id # Agora é um Inteiro correto

    new_session = TableSession(
        company_id=company_id,
        table_id=table.id,
        customer_name=data.customer_name,
        session_token=str(uuid.uuid4()),
        access_pin="0000",
        is_active=True,
        opened_by_employee_id=opener_id
    )
    db.add(new_session)
    db.commit()
    return {"message": "Mesa aberta"}

@router.post("/{table_id}/close", status_code=200)
async def close_table_session(
    table_id: int,
    data: CloseTableRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug
    
    session = db.query(TableSession).filter(
        TableSession.table_id == table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()
    
    if not session: raise HTTPException(404, "Nenhuma sessão ativa")
    
    orders = db.query(Order).filter(Order.session_id == session.id).all()
    total_amount = sum(o.total_amount for o in orders)
    
    # 1. Calcular Gorjeta (Service Fee)
    company = db.query(Company).filter(Company.id == company_id).first()
    service_fee_pct = company.service_fee_percentage or Decimal(0)
    
    if service_fee_pct > 0 and total_amount > 0:
        # Calcula 10% sobre o total
        tip_amount = (total_amount * (service_fee_pct / Decimal(100))).quantize(Decimal("0.01"))
        
        # Se a mesa foi aberta por um funcionário, credita a ele
        if session.opened_by_employee_id:
            ledger_entry = ServiceFeeLedger(
                company_id=company_id,
                employee_id=session.opened_by_employee_id,
                amount=tip_amount
            )
            db.add(ledger_entry)

    # 2. Lógica de Comissão SaaS (Split)
    if data.payment_method in [PaymentMethod.CASH, PaymentMethod.CARD]:
        if company.marketplace_fee_percentage > 0:
            fee = (total_amount * (company.marketplace_fee_percentage / Decimal(100))).quantize(Decimal("0.01"))
            if company.pending_commission_balance is None:
                company.pending_commission_balance = Decimal(0)
            company.pending_commission_balance += fee

    for order in orders:
        order.payment_status = PaymentStatus.PAID
        order.payment_method = data.payment_method
        if order.status == OrderStatus.PENDING:
            order.status = OrderStatus.ACCEPTED
            
    session.is_active = False
    session.closed_at = datetime.now()
    
    requests = db.query(ServiceRequest).filter(ServiceRequest.table_id == table_id, ServiceRequest.status == "pending").all()
    for req in requests:
        req.status = "resolved"
        
    db.commit()
    await manager.broadcast({"type": "order_update", "table_id": table_id}, slug)
    return {"message": "Mesa fechada"}

@router.patch("/positions", status_code=200)
def update_table_positions(
    positions: List[TablePositionUpdate],
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    for pos in positions:
        table = db.query(Table).filter(Table.id == pos.id, Table.company_id == company_id).first()
        if table:
            table.position_x = pos.x
            table.position_y = pos.y
    db.commit()
    return {"message": "Layout atualizado"}

@router.patch("/sessions/{session_id}", status_code=200)
def update_session_name(
    session_id: int,
    data: SessionUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    session = db.query(TableSession).filter(TableSession.id == session_id, TableSession.company_id == company_id).first()
    if not session:
        raise HTTPException(404, "Sessão não encontrada")
    session.customer_name = data.customer_name
    db.commit()
    return {"message": "Nome atualizado"}

@router.get("/sessions/{session_id}/details", response_model=TableSessionDetail)
def get_session_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    session = db.query(TableSession).options(
        selectinload(TableSession.orders).selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(TableSession.orders).selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(TableSession.id == session_id, TableSession.company_id == company_id).first()
    if not session:
        raise HTTPException(404, "Sessão não encontrada")
    total = sum(o.total_amount for o in session.orders)
    return {
        "id": session.id,
        "customer_name": session.customer_name,
        "total_spent": total,
        "start_time": session.created_at,
        "orders": session.orders
    }

@router.post("/transfer", status_code=200)
async def transfer_table(
    data: TableTransferRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    slug = current_user.slug if isinstance(current_user, Company) else current_user.company.slug

    from_session = db.query(TableSession).filter(
        TableSession.table_id == data.from_table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()

    if not from_session:
        raise HTTPException(404, "Mesa de origem não tem sessão ativa")

    to_table = db.query(Table).filter(Table.id == data.to_table_id, Table.company_id == company_id).first()
    if not to_table:
        raise HTTPException(404, "Mesa de destino não encontrada")

    to_session = db.query(TableSession).filter(
        TableSession.table_id == data.to_table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()

    if to_session:
        if not data.merge:
            raise HTTPException(409, "Mesa de destino ocupada. Deseja juntar?")
        
        orders = db.query(Order).filter(Order.session_id == from_session.id).all()
        for order in orders:
            order.session_id = to_session.id
            order.table_id = to_table.id
        
        requests = db.query(ServiceRequest).filter(ServiceRequest.table_id == data.from_table_id, ServiceRequest.status == "pending").all()
        for req in requests:
            req.table_id = to_table.id

        from_session.is_active = False
        from_session.closed_at = datetime.now()
        db.commit()
        
        await manager.broadcast({"type": "order_update", "message": "Mesas unificadas"}, slug)
        return {"message": f"Mesas unificadas em {to_table.table_number}"}

    else:
        from_session.table_id = to_table.id
        
        orders = db.query(Order).filter(Order.session_id == from_session.id).all()
        for order in orders:
            order.table_id = to_table.id
            
        requests = db.query(ServiceRequest).filter(ServiceRequest.table_id == data.from_table_id, ServiceRequest.status == "pending").all()
        for req in requests:
            req.table_id = to_table.id

        db.commit()
        await manager.broadcast({"type": "order_update", "message": "Mesa transferida"}, slug)
        return {"message": f"Transferido para Mesa {to_table.table_number}"}