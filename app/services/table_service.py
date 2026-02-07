# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 07:40:00
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from typing import List, Optional
import uuid
import random
import string
from datetime import datetime
from decimal import Decimal
from app.models import (
    Table, TableSession, Order, ServiceRequest, 
    OrderStatus, PaymentStatus, ServiceFeeLedger, Company, Employee, OrderItem
)
from app.services.payment_service import PaymentService

class TableService:
    def __init__(self):
        self.payment_service = PaymentService()

    def _generate_secure_pin(self, length: int = 10) -> str:
        return ''.join(random.choices(string.digits, k=length))

    def get_all_tables(self, db: Session, company_id: str) -> List[Table]:
        return db.query(Table).filter(Table.company_id == company_id).order_by(Table.table_number).all()

    def create_table(self, db: Session, company_id: str, table_number: int) -> Table:
        if db.query(Table).filter(Table.company_id == company_id, Table.table_number == table_number).first():
            raise HTTPException(status_code=400, detail="Número de mesa já existe")
        
        new_table = Table(
            company_id=company_id,
            table_number=table_number,
            qr_token=str(uuid.uuid4()),
            is_active=True
        )
        db.add(new_table)
        db.commit()
        db.refresh(new_table)
        return new_table

    def bulk_create(self, db: Session, company_id: str, start: int, end: int) -> int:
        created_count = 0
        for num in range(start, end + 1):
            if not db.query(Table).filter(Table.company_id == company_id, Table.table_number == num).first():
                db.add(Table(
                    company_id=company_id,
                    table_number=num,
                    qr_token=str(uuid.uuid4()),
                    is_active=True
                ))
                created_count += 1
        db.commit()
        return created_count

    def update_positions(self, db: Session, company_id: str, positions: List[any]):
        for pos in positions:
            db.query(Table).filter(Table.id == pos.id, Table.company_id == company_id).update({
                "position_x": pos.x,
                "position_y": pos.y
            })
        db.commit()

    def get_dashboard_data(self, db: Session, company_id: str) -> List[dict]:
        tables = self.get_all_tables(db, company_id)
        dashboard_data = []
        
        for table in tables:
            active_session = db.query(TableSession).filter(
                TableSession.table_id == table.id, 
                TableSession.is_active == True
            ).first()
            
            active_request = db.query(ServiceRequest).filter(
                ServiceRequest.table_id == table.id, 
                ServiceRequest.status == "pending"
            ).first()
            
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

    def open_session(self, db: Session, table_id: int, company_id: str, customer_name: str, opener_id: Optional[int]) -> str:
        table = db.query(Table).filter(Table.id == table_id, Table.company_id == company_id).first()
        if not table: 
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
            
        existing = db.query(TableSession).filter(TableSession.table_id == table_id, TableSession.is_active == True).first()
        if existing: 
            raise HTTPException(status_code=400, detail="Mesa já está ocupada")
            
        pin = self._generate_secure_pin(10)
        new_session = TableSession(
            company_id=company_id,
            table_id=table_id,
            customer_name=customer_name,
            session_token=str(uuid.uuid4()),
            access_pin=pin,
            is_active=True,
            opened_by_employee_id=opener_id
        )
        db.add(new_session)
        db.commit()
        return pin

    def process_partial_payment(self, db: Session, table_id: int, company_id: str, amount: Decimal, method: str) -> dict:
        session = db.query(TableSession).filter(
            TableSession.table_id == table_id,
            TableSession.is_active == True,
            TableSession.company_id == company_id
        ).first()
        
        if not session: 
            raise HTTPException(status_code=404, detail="Nenhuma sessão ativa")
            
        orders = db.query(Order).filter(
            Order.session_id == session.id,
            Order.payment_status != PaymentStatus.PAID
        ).order_by(Order.created_at.asc()).all()
        
        remaining_payment = amount
        paid_orders_count = 0
        
        for order in orders:
            if remaining_payment <= 0: break
            
            if remaining_payment >= order.total_amount:
                order.payment_status = PaymentStatus.PAID
                order.payment_method = method
                remaining_payment -= order.total_amount
                paid_orders_count += 1
                
        db.commit()
        return {
            "paid_count": paid_orders_count,
            "remaining": remaining_payment
        }

    async def close_session(self, db: Session, table_id: int, company: Company, payment_method: str, custom_fee: Optional[float]):
        session = db.query(TableSession).filter(
            TableSession.table_id == table_id,
            TableSession.is_active == True,
            TableSession.company_id == company.id
        ).first()
        
        if not session: 
            raise HTTPException(status_code=404, detail="Nenhuma sessão ativa")
            
        orders = db.query(Order).filter(
            Order.session_id == session.id,
            Order.payment_status != PaymentStatus.PAID
        ).all()
        
        total_amount = sum(o.total_amount for o in orders)
        pix_data = None
        
        if payment_method == "pix" and total_amount > 0:
            if company.payment_provider != "none":
                mock_order = Order(id=str(uuid.uuid4()), total_amount=total_amount, customer_name=session.customer_name)
                pix_data = await self.payment_service.create_pix_payment(mock_order, company)
        
        # Lógica de Gorjeta
        service_fee_pct = company.service_fee_percentage or Decimal(0)
        tip_amount = Decimal(0)
        
        if custom_fee is not None:
            tip_amount = Decimal(str(custom_fee))
        else:
            all_orders = db.query(Order).filter(Order.session_id == session.id).all()
            total_consumption = sum(o.total_amount for o in all_orders)
            tip_amount = (total_consumption * (service_fee_pct / Decimal(100))).quantize(Decimal("0.01"))
            
        if tip_amount > 0 and session.opened_by_employee_id:
            db.add(ServiceFeeLedger(
                company_id=company.id, 
                employee_id=session.opened_by_employee_id, 
                amount=tip_amount,
                created_at=datetime.now()
            ))
            
        for order in orders:
            order.payment_status = PaymentStatus.PAID
            order.payment_method = payment_method
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.ACCEPTED
                
        session.is_active = False
        session.closed_at = datetime.now()
        
        db.query(ServiceRequest).filter(
            ServiceRequest.table_id == table_id, 
            ServiceRequest.status == "pending"
        ).update({"status": "resolved"})
        
        db.commit()
        return pix_data

    def transfer_or_merge(self, db: Session, company_id: str, from_id: int, to_id: int, merge: bool):
        source_session = db.query(TableSession).filter(
            TableSession.table_id == from_id,
            TableSession.is_active == True,
            TableSession.company_id == company_id
        ).first()
        
        if not source_session: 
            raise HTTPException(status_code=404, detail="Mesa de origem não tem sessão ativa")
            
        target_session = db.query(TableSession).filter(
            TableSession.table_id == to_id,
            TableSession.is_active == True,
            TableSession.company_id == company_id
        ).first()
        
        if target_session:
            if not merge:
                raise HTTPException(status_code=409, detail=f"Mesa de destino ocupada por {target_session.customer_name}. Deseja juntar?")
            
            db.query(Order).filter(Order.session_id == source_session.id).update({
                "session_id": target_session.id, 
                "table_id": to_id
            })
            
            source_session.is_active = False
            source_session.closed_at = datetime.now()
        else:
            source_session.table_id = to_id
            db.query(Order).filter(Order.session_id == source_session.id).update({
                "table_id": to_id
            })
            
        db.commit()

    def delete_table(self, db: Session, company_id: str, table_id: int):
        """
        Exclui uma mesa se ela não estiver ocupada.
        """
        table = db.query(Table).filter(
            Table.id == table_id,
            Table.company_id == company_id
        ).first()

        if not table:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")

        # Verifica se há sessão ativa
        active_session = db.query(TableSession).filter(
            TableSession.table_id == table.id,
            TableSession.is_active == True
        ).first()

        if active_session:
            raise HTTPException(status_code=400, detail="Não é possível excluir uma mesa ocupada. Feche a conta primeiro.")

        db.delete(table)
        db.commit()
