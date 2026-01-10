# DOMAIN: BACKEND
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user
from app.models import Company
from app.services.ai_prediction_service import AiPredictionService

router = APIRouter()

@router.get("/forecast")
def get_sales_forecast(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Retorna a previsão de vendas para os próximos N dias.
    """
    # Identificar Company ID
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    try:
        result = AiPredictionService.predict_sales(db, str(company_id), days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na previsão de IA: {str(e)}")
