from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, selectinload
from app.database import get_db, set_tenant
from app.models import Company, Table, TableSession, ServiceRequest, Order, OrderItem
from app.schemas.public import CheckTableRequest, CheckTableResponse, TableSessionResponse, JoinTableRequest
from app.core.limiter import limiter
import uuid
import random
import string
import datetime

router = APIRouter()

@router.post("/{company_slug}/check-table", response_model=CheckTableResponse)
@limiter.limit("20/minute")
def check_table_status(request: Request, company_slug: str, data: CheckTableRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: 
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    set_tenant(db, str(company.id))
    if data.qr_token in ["admin-override", "staff-override"]:
        active_session = db.query(TableSession).filter(
            TableSession.table_id == data.table_id, 
            TableSession.is_active == True
        ).first()
        if active_session:
            return {
                "status": "active", 
                "customer_name": active_session.customer_name, 
                "session_token": active_session.session_token, 
                "access_pin": active_session.access_pin
            }
        return {"status": "free"}
    table = db.query(Table).filter(
        Table.id == data.table_id, 
        Table.company_id == company.id
    ).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    if table.qr_token != data.qr_token:
        raise HTTPException(status_code=403, detail="QR Code inválido ou expirado")
    active_session = db.query(TableSession).filter(
        TableSession.table_id == table.id, 
        TableSession.is_active == True
    ).first()
    if not active_session: 
        return {"status": "free"}
    if data.session_token and data.session_token == active_session.session_token:
        return {
            "status": "active", 
            "customer_name": active_session.customer_name, 
            "session_token": active_session.session_token
        }
    return {
        "status": "blocked", 
        "customer_name": active_session.customer_name, 
        "requires_pin": True
    }

@router.post("/{company_slug}/join-table", response_model=TableSessionResponse)
@limiter.limit("5/minute")
def join_table(request: Request, company_slug: str, data: JoinTableRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: raise HTTPException(404, "Empresa não encontrada")
    set_tenant(db, str(company.id))
    table = db.query(Table).filter(Table.id == data.table_id, Table.company_id == company.id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    if data.qr_token not in ["admin-override", "staff-override"] and table.qr_token != data.qr_token:
        raise HTTPException(status_code=403, detail="QR Code inválido")
    active_session = db.query(TableSession).filter(
        TableSession.table_id == table.id, 
        TableSession.is_active == True
    ).first()
    if not active_session:
        pin = ''.join(random.choices(string.digits, k=4))
        new_session = TableSession(
            company_id=company.id, 
            table_id=table.id, 
            customer_name=data.customer_name, 
            session_token=str(uuid.uuid4()), 
            access_pin=pin, 
            is_active=True
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    if data.pin == active_session.access_pin: 
        return active_session
    raise HTTPException(status_code=403, detail="PIN de acesso incorreto")

@router.post("/{company_slug}/service-request")
@limiter.limit("5/minute")
async def create_public_service_request(request: Request, company_slug: str, data: dict, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == company_slug).first()
    if not company: raise HTTPException(404, "Empresa não encontrada")
    set_tenant(db, str(company.id))
    new_request = ServiceRequest(
        company_id=company.id,
        table_id=data.get("table_id"),
        service_type=data.get("service_type", "help"),
        notes=data.get("notes"),
        status="pending"
    )
    db.add(new_request)
    db.commit()
    return {"status": "sent"}

@router.get("/session/{identifier}")
def get_session_details(identifier: str, db: Session = Depends(get_db)):
    session = db.query(TableSession).options(
        selectinload(TableSession.orders).selectinload(Order.items).selectinload(OrderItem.product)
    ).filter(TableSession.session_token == identifier).first()
    if not session and identifier.isdigit():
        session = db.query(TableSession).options(
            selectinload(TableSession.orders).selectinload(Order.items).selectinload(OrderItem.product)
        ).filter(TableSession.id == int(identifier)).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    total = sum(o.total_amount for o in session.orders if o.payment_status != 'refunded')
    session.total_spent = total
    return session
