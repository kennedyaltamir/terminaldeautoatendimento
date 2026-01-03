from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
from app.database import get_db
from app.models import Company, Table, TableSession, Order, ServiceRequest, OrderStatus, PaymentStatus
from app.schemas import TableResponse, TableCreate, TableBulkCreate, TableDashboardResponse, OpenTableRequest, CloseTableRequest, TablePositionUpdate
from app.routers.auth import get_current_user
from app.websockets import manager

router = APIRouter()

@router.get("", response_model=List[TableResponse])
def get_tables(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """Lista todas as mesas da empresa (Simples)"""
    return db.query(Table).filter(Table.company_id == current_user.id).order_by(Table.table_number).all()

@router.post("", response_model=TableResponse, status_code=201)
def create_table(
    table_data: TableCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """Cria uma nova mesa com token automático"""
    exists = db.query(Table).filter(
        Table.company_id == current_user.id,
        Table.table_number == table_data.table_number
    ).first()
    
    if exists:
        raise HTTPException(status_code=400, detail=f"Mesa {table_data.table_number} já existe")

    new_table = Table(
        company_id=current_user.id,
        table_number=table_data.table_number,
        qr_token=uuid.uuid4().hex
    )
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

@router.post("/bulk", status_code=201)
def create_tables_bulk(
    bulk_data: TableBulkCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    if bulk_data.start > bulk_data.end:
        raise HTTPException(status_code=400, detail="O início deve ser menor que o fim")
    
    if (bulk_data.end - bulk_data.start) > 100:
        raise HTTPException(status_code=400, detail="Máximo de 100 mesas por vez")

    created_count = 0
    
    for num in range(bulk_data.start, bulk_data.end + 1):
        exists = db.query(Table).filter(
            Table.company_id == current_user.id,
            Table.table_number == num
        ).first()
        
        if not exists:
            new_table = Table(
                company_id=current_user.id,
                table_number=num,
                qr_token=uuid.uuid4().hex
            )
            db.add(new_table)
            created_count += 1
    
    db.commit()
    return {"message": f"{created_count} mesas criadas com sucesso"}

@router.delete("/{table_id}", status_code=204)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    table = db.query(Table).filter(
        Table.id == table_id,
        Table.company_id == current_user.id
    ).first()

    if not table:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    
    db.delete(table)
    db.commit()
    return None

# --- NOVAS ROTAS DE GESTÃO OPERACIONAL ---

@router.get("/dashboard", response_model=List[TableDashboardResponse])
def get_tables_dashboard(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """Retorna o status em tempo real de todas as mesas"""
    tables = db.query(Table).filter(Table.company_id == current_user.id).order_by(Table.table_number).all()
    
    dashboard_data = []
    
    for table in tables:
        # 1. Buscar Sessão Ativa
        active_session = db.query(TableSession).filter(
            TableSession.table_id == table.id,
            TableSession.is_active == True
        ).first()
        
        # 2. Buscar Chamado Pendente
        active_request = db.query(ServiceRequest).filter(
            ServiceRequest.table_id == table.id,
            ServiceRequest.status == "pending"
        ).first()
        
        status = "free"
        session_summary = None
        
        if active_session:
            status = "occupied"
            # Calcular total gasto na sessão
            orders = db.query(Order).filter(Order.session_id == active_session.id).all()
            total = sum(o.total_amount for o in orders)
            
            session_summary = {
                "id": active_session.id,
                "customer_name": active_session.customer_name,
                "total_spent": total,
                "start_time": active_session.created_at
            }
            
        if active_request:
            status = "alert" # Prioridade visual para alertas
            
        dashboard_data.append({
            "id": table.id,
            "table_number": table.table_number,
            "qr_token": table.qr_token,
            "status": status,
            "position_x": table.position_x, # --- NOVO ---
            "position_y": table.position_y, # --- NOVO ---
            "active_session": session_summary,
            "service_request": active_request.service_type if active_request else None
        })
        
    return dashboard_data

@router.post("/{table_id}/open", status_code=200)
def open_table_session(
    table_id: int,
    data: OpenTableRequest,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    table = db.query(Table).filter(Table.id == table_id, Table.company_id == current_user.id).first()
    if not table: raise HTTPException(404, "Mesa não encontrada")
    
    # Verifica se já tem sessão
    existing = db.query(TableSession).filter(TableSession.table_id == table.id, TableSession.is_active == True).first()
    if existing: raise HTTPException(400, "Mesa já está ocupada")
    
    new_session = TableSession(
        company_id=current_user.id,
        table_id=table.id,
        customer_name=data.customer_name,
        session_token=str(uuid.uuid4()),
        access_pin="0000" # PIN padrão para abertura manual
    )
    db.add(new_session)
    db.commit()
    return {"message": "Mesa aberta com sucesso"}

@router.post("/{table_id}/close", status_code=200)
async def close_table_session(
    table_id: int,
    data: CloseTableRequest,
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    session = db.query(TableSession).filter(
        TableSession.table_id == table_id,
        TableSession.is_active == True,
        TableSession.company_id == current_user.id
    ).first()
    
    if not session: raise HTTPException(404, "Nenhuma sessão ativa nesta mesa")
    
    # 1. Atualizar todos os pedidos pendentes para PAGO
    orders = db.query(Order).filter(Order.session_id == session.id).all()
    for order in orders:
        if order.payment_status != PaymentStatus.PAID:
            order.payment_status = PaymentStatus.PAID
            order.payment_method = data.payment_method # Atualiza com o método real do fechamento
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.ACCEPTED # Se estava pendente, aceita
    
    # 2. Fechar Sessão
    session.is_active = False
    session.closed_at = datetime.now()
    
    # 3. Resolver chamados pendentes
    requests = db.query(ServiceRequest).filter(ServiceRequest.table_id == table_id, ServiceRequest.status == "pending").all()
    for req in requests:
        req.status = "resolved"
    
    db.commit()
    
    # Notificar KDS para limpar alertas e atualizar status
    await manager.broadcast({
        "type": "order_update", 
        "table_id": table_id
    }, current_user.slug)
    
    return {"message": "Mesa fechada e liberada"}

# --- NOVO ENDPOINT PARA ATUALIZAR POSIÇÕES ---
@router.patch("/positions", status_code=200)
def update_table_positions(
    positions: List[TablePositionUpdate],
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    for pos in positions:
        table = db.query(Table).filter(Table.id == pos.id, Table.company_id == current_user.id).first()
        if table:
            table.position_x = pos.x
            table.position_y = pos.y
    
    db.commit()
    return {"message": "Layout atualizado"}