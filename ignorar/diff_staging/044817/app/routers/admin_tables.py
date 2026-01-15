# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 04:45:00
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import random
import string
from datetime import datetime
from decimal import Decimal
from app.database import get_db
from app.models import Company, Table, TableSession, Order, ServiceRequest, OrderStatus, PaymentStatus, PaymentMethod, ServiceFeeLedger, Employee
from app.schemas import (
    TableResponse, TableCreate, TableBulkCreate, TableDashboardResponse, 
    OpenTableRequest, CloseTableRequest, TablePositionUpdate, 
    SessionUpdate, TableSessionDetail, TableTransferRequest
)
from app.routers.auth import get_current_user
from app.websockets import manager
from app.services.payment_service import PaymentService
from pydantic import BaseModel

router = APIRouter()
payment_service = PaymentService()

class PartialPaymentRequest(BaseModel):
    amount: Decimal
    payment_method: str

def generate_secure_pin(length: int = 10) -> str:
    return ''.join(random.choices(string.digits, k=length))

# --- CRUD BÁSICO (Normalizado com prefixo /tables para o Frontend) ---

@router.get("/tables", response_model=List[TableResponse])
def get_tables(
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    return db.query(Table).filter(Table.company_id == company_id).order_by(Table.table_number).all()

@router.post("/tables", response_model=TableResponse, status_code=201)
def create_table(
    data: TableCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    if db.query(Table).filter(Table.company_id == company_id, Table.table_number == data.table_number).first():
        raise HTTPException(400, "Número de mesa já existe")
    new_table = Table(
        company_id=company_id,
        table_number=data.table_number,
        qr_token=str(uuid.uuid4())
    )
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.post("/tables/bulk", status_code=201)
def create_tables_bulk(
    data: TableBulkCreate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    created_count = 0
    for num in range(data.start, data.end + 1):
        if not db.query(Table).filter(Table.company_id == company_id, Table.table_number == num).first():
            db.add(Table(
                company_id=company_id,
                table_number=num,
                qr_token=str(uuid.uuid4())
            ))
            created_count += 1
    db.commit()
    return {"message": f"{created_count} mesas criadas"}

@router.delete("/tables/{table_id}", status_code=204)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    table = db.query(Table).filter(Table.id == table_id, Table.company_id == company_id).first()
    if not table:
        raise HTTPException(404, "Mesa não encontrada")
    db.delete(table)
    db.commit()
    return None

@router.patch("/tables/positions", status_code=200)
def update_table_positions(
    positions: List[TablePositionUpdate],
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    for pos in positions:
        db.query(Table).filter(Table.id == pos.id, Table.company_id == company_id).update({
            "position_x": pos.x,
            "position_y": pos.y
        })
    db.commit()
    return {"message": "Posições atualizadas"}

# --- DASHBOARD & OPERAÇÃO ---

@router.get("/tables/dashboard", response_model=List[TableDashboardResponse])
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
            orders = db.query(Order).filter(
                Order.session_id == active_session.id,
                Order.payment_status != PaymentStatus.PAID
            ).all()
            total = sum(o.total_amount for o in orders)
            session_summary = {
                "id": active_session.id,
                "customer_name": active_session.customer_name,
                "total_spent": total,
                "start_time": active_session.created_at,
                "access_pin": active_session.access_pin 
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

@router.post("/tables/{table_id}/open", status_code=200)
async def open_table_session(
    table_id: int,
    data: OpenTableRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company = current_user if isinstance(current_user, Company) else current_user.company
    company_id = company.id
    table = db.query(Table).filter(Table.id == table_id, Table.company_id == company_id).first()
    if not table: raise HTTPException(404, "Mesa não encontrada")
    existing = db.query(TableSession).filter(TableSession.table_id == table.id, TableSession.is_active == True).first()
    if existing: raise HTTPException(400, "Mesa já está ocupada")
    opener_id = current_user.id if isinstance(current_user, Employee) else None
    pin = generate_secure_pin(10)
    new_session = TableSession(
        company_id=company_id,
        table_id=table.id,
        customer_name=data.customer_name,
        session_token=str(uuid.uuid4()),
        access_pin=pin,
        is_active=True,
        opened_by_employee_id=opener_id
    )
    db.add(new_session)
    db.commit()
    await manager.broadcast({"type": "order_update", "table_id": table_id}, company.slug)
    return {"message": "Mesa aberta", "pin": pin}

@router.post("/tables/{table_id}/pay", status_code=200)
async def pay_table_partial(
    table_id: int,
    data: PartialPaymentRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company = current_user if isinstance(current_user, Company) else current_user.company
    company_id = company.id
    session = db.query(TableSession).filter(
        TableSession.table_id == table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()
    if not session: raise HTTPException(404, "Nenhuma sessão ativa")
    orders = db.query(Order).filter(
        Order.session_id == session.id,
        Order.payment_status != PaymentStatus.PAID
    ).order_by(Order.created_at.asc()).all()
    remaining_payment = data.amount
    paid_orders_count = 0
    for order in orders:
        if remaining_payment <= 0: break
        if remaining_payment >= order.total_amount:
            order.payment_status = PaymentStatus.PAID
            order.payment_method = data.payment_method
            remaining_payment -= order.total_amount
            paid_orders_count += 1
    db.commit()
    await manager.broadcast({"type": "order_update", "table_id": table_id}, company.slug)
    return {
        "message": f"Pagamento de R$ {data.amount} processado.",
        "orders_paid": paid_orders_count,
        "remaining_credit": remaining_payment
    }

@router.post("/tables/{table_id}/close", status_code=200)
async def close_table_session(
    table_id: int,
    data: CloseTableRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company = current_user if isinstance(current_user, Company) else current_user.company
    company_id = company.id
    slug = company.slug
    session = db.query(TableSession).filter(
        TableSession.table_id == table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()
    if not session: raise HTTPException(404, "Nenhuma sessão ativa")
    orders = db.query(Order).filter(
        Order.session_id == session.id,
        Order.payment_status != PaymentStatus.PAID
    ).all()
    total_amount = sum(o.total_amount for o in orders)
    pix_data = None
    if data.payment_method == "pix" and total_amount > 0:
        try:
            if company.payment_provider != "NONE":
                mock_order = Order(id=uuid.uuid4(), total_amount=total_amount, customer_name=session.customer_name)
                pix_data = await payment_service.create_pix_payment(mock_order, company)
        except Exception as e:
            print(f"Erro ao gerar Pix: {e}")
    service_fee_pct = company.service_fee_percentage or Decimal(0)
    if data.custom_service_fee is not None:
        tip_amount = data.custom_service_fee
    else:
        all_orders = db.query(Order).filter(Order.session_id == session.id).all()
        total_consumption = sum(o.total_amount for o in all_orders)
        tip_amount = (total_consumption * (service_fee_pct / Decimal(100))).quantize(Decimal("0.01"))
    if tip_amount > 0 and session.opened_by_employee_id:
        db.add(ServiceFeeLedger(company_id=company_id, employee_id=session.opened_by_employee_id, amount=tip_amount))
    for order in orders:
        order.payment_status = PaymentStatus.PAID
        order.payment_method = data.payment_method
        if order.status == OrderStatus.PENDING:
            order.status = OrderStatus.ACCEPTED
    session.is_active = False
    session.closed_at = datetime.now()
    db.query(ServiceRequest).filter(ServiceRequest.table_id == table_id, ServiceRequest.status == "pending").update({"status": "resolved"})
    db.commit()
    await manager.broadcast({"type": "order_update", "table_id": table_id}, slug)
    return {"message": "Mesa fechada", "pix_data": pix_data}

@router.patch("/tables/sessions/{session_id}", status_code=200)
def update_session_name(
    session_id: int,
    data: SessionUpdate,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    session = db.query(TableSession).filter(TableSession.id == session_id, TableSession.company_id == company_id).first()
    if not session: raise HTTPException(404, "Sessão não encontrada")
    session.customer_name = data.customer_name
    db.commit()
    return {"message": "Nome atualizado"}

@router.get("/tables/sessions/{session_id}/details", response_model=TableSessionDetail)
def get_session_details(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    session = db.query(TableSession).filter(TableSession.id == session_id, TableSession.company_id == company_id).first()
    if not session: raise HTTPException(404, "Sessão não encontrada")
    orders = db.query(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product),
        selectinload(Order.items).selectinload(OrderItem.selected_options)
    ).filter(Order.session_id == session.id).all()
    total = sum(o.total_amount for o in orders)
    return {
        "id": session.id,
        "customer_name": session.customer_name,
        "total_spent": total,
        "start_time": session.created_at,
        "orders": orders
    }

@router.post("/tables/transfer", status_code=200)
def transfer_table(
    data: TableTransferRequest,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    source_session = db.query(TableSession).filter(
        TableSession.table_id == data.from_table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()
    if not source_session: raise HTTPException(404, "Mesa de origem não tem sessão ativa")
    target_session = db.query(TableSession).filter(
        TableSession.table_id == data.to_table_id,
        TableSession.is_active == True,
        TableSession.company_id == company_id
    ).first()
    if target_session:
        if not data.merge:
            raise HTTPException(409, detail=f"Mesa de destino ocupada por {target_session.customer_name}. Deseja juntar?")
        db.query(Order).filter(Order.session_id == source_session.id).update({"session_id": target_session.id, "table_id": data.to_table_id})
        source_session.is_active = False
        source_session.closed_at = datetime.now()
        db.commit()
        return {"message": "Mesas unificadas com sucesso"}
    else:
        source_session.table_id = data.to_table_id
        db.query(Order).filter(Order.session_id == source_session.id).update({"table_id": data.to_table_id})
        db.commit()
        return {"message": "Mesa transferida com sucesso"}
