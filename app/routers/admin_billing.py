from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company
from app.routers.auth import get_current_user
from app.services.stripe_service import StripeService
from app.schemas import StripeCheckoutResponse

router = APIRouter()

@router.post("/upgrade", response_model=StripeCheckoutResponse)
def upgrade_to_pro(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    if not isinstance(current_user, Company):
        raise HTTPException(status_code=403, detail="Apenas o dono pode assinar planos")
        
    try:
        checkout_url = StripeService.create_checkout_session(current_user)
        db.commit() 
        return {"url": checkout_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/portal", response_model=StripeCheckoutResponse)
def manage_billing(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    if not isinstance(current_user, Company):
        raise HTTPException(status_code=403, detail="Apenas o dono pode gerenciar a assinatura")

    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="Nenhuma conta de faturamento encontrada")
        
    try:
        portal_url = StripeService.create_portal_session(current_user)
        return {"url": portal_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))