from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
import uuid
import time

from app.database import get_db
from app.models import Order, PaymentStatus, OrderStatus

router = APIRouter()

class PaymentRequest(BaseModel):
    order_id: UUID
    card_number: str
    card_holder: str
    expiration: str
    cvv: str

@router.post("/process", status_code=200)
def process_payment(
    payment_data: PaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Simula o processamento de um pagamento online.
    Em produção, aqui chamaríamos Stripe/MercadoPago.
    """

    # 1. Buscar o pedido (O Pydantic já converteu order_id para UUID)
    order = db.query(Order).filter(Order.id == payment_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.payment_status == PaymentStatus.PAID:
        return {"status": "already_paid", "message": "Pedido já foi pago"}

    # 2. Simular latência do banco (1 segundo)
    time.sleep(1)

    # 3. Simular Validação (Rejeita cartão terminado em 0000)
    if payment_data.card_number.endswith("0000"):
        order.payment_status = PaymentStatus.FAILED
        db.commit()
        raise HTTPException(status_code=400, detail="Pagamento recusado pela operadora")

    # 4. Sucesso: Atualizar Status
    order.payment_status = PaymentStatus.PAID

    # Se pagou online, o pedido é aceito automaticamente (pula a etapa de "Aceitar" do garçom)
    if order.status == OrderStatus.PENDING:
        order.status = OrderStatus.ACCEPTED

    db.commit()

    return {
        "status": "approved",
        "transaction_id": f"tx_{uuid.uuid4().hex[:12]}",
        "message": "Pagamento aprovado com sucesso"
    }
