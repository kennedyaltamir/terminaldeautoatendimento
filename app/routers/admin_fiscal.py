from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Company, Order, FiscalStatus
from app.schemas import FiscalEmissionResponse
from app.routers.auth import get_current_user
from app.services.fiscal_service import FiscalService

router = APIRouter()

def require_admin(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    if hasattr(current_user, "role") and current_user.role in ["manager", "owner"]:
        return current_user
    raise HTTPException(status_code=403, detail="Sem permissão fiscal")

@router.post("/orders/{order_id}/emit", response_model=FiscalEmissionResponse)
async def emit_fiscal_document(
    order_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: any = Depends(require_admin)
):
    # Identificar Company ID
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    # Buscar Pedido
    order = db.query(Order).filter(Order.id == order_id, Order.company_id == company_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.fiscal_status in [FiscalStatus.EMITTED, FiscalStatus.PROCESSING]:
        return {
            "status": "success",
            "message": "Nota já emitida ou em processamento",
            "nfe_url": order.nfe_url_pdf
        }

    # Atualiza status para processando imediatamente para feedback visual
    order.fiscal_status = FiscalStatus.PROCESSING
    db.commit()

    # Enfileira a tarefa pesada (passando SessionLocal para criar nova sessão na thread)
    background_tasks.add_task(
        FiscalService.process_emission, 
        str(order.id), 
        str(company_id), 
        SessionLocal
    )
    
    return {
        "status": "processing",
        "message": "Emissão solicitada. Aguarde o processamento.",
        "nfe_url": None
    }