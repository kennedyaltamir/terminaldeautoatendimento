# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-26 00:25:00
# DESCRIPTION: Router Fiscal endurecido com captura de ID resiliente.

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Order, FiscalStatus
from app.schemas import FiscalEmissionResponse
from app.routers.auth import get_current_user
from app.services.fiscal_service import FiscalService
import logging

logger = logging.getLogger("FiscalRouter")
router = APIRouter()

@router.post("/orders/{order_id}/emit", response_model=FiscalEmissionResponse)
async def emit_fiscal_document(
    order_id: str, # FIX: Usar str para evitar 404 de validação de tipo no path
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """Solicita a emissão de nota fiscal para um pedido."""
    company_id = current_user.id if hasattr(current_user, 'owner_email') else current_user.company_id
    
    # Busca o pedido validando o tenant
    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()
    
    if not order:
        logger.warning(f"Pedido {order_id} não encontrado para o tenant {company_id}")
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.fiscal_status in ["emitted", "processing"]:
        return {"status": "success", "message": "Nota já processada", "nfe_url": order.nfe_url_pdf}

    order.fiscal_status = "processing"
    db.commit()

    background_tasks.add_task(FiscalService.process_emission, str(order.id), str(company_id), SessionLocal)
    return {"status": "processing", "message": "Emissão em andamento."}
