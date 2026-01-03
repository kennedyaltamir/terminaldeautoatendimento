from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, PaymentStatus, OrderStatus
from app.websockets import manager # <--- Importar
import httpx

router = APIRouter()

@router.post("/mercadopago")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    params = request.query_params
    topic = params.get("topic") or params.get("type")
    resource_id = params.get("id") or params.get("data.id")

    if topic == "payment" and resource_id:
        order = db.query(Order).filter(Order.mp_payment_id == resource_id).first()
        
        if order:
            print(f"💰 Webhook recebido para Pedido {order.id}. Atualizando para PAGO.")
            order.payment_status = PaymentStatus.PAID
            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.ACCEPTED
            
            db.commit()

            # --- NOTIFICAÇÃO WS ---
            # Precisamos do slug da empresa. Como o webhook não tem user logado,
            # fazemos um join ou lazy load. O SQLAlchemy já carrega 'company' se configurado.
            # Vamos garantir carregando a empresa.
            if order.company:
                await manager.broadcast({
                    "type": "order_update",
                    "order_id": str(order.id),
                    "status": order.status,
                    "payment_status": order.payment_status
                }, order.company.slug)
            # ----------------------

            return {"status": "updated"}
            
    return {"status": "ignored"}