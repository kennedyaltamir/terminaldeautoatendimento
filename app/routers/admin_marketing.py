from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Company
from app.routers.auth import get_current_user
from app.services.recommendation_service import RecommendationService

router = APIRouter()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    raise HTTPException(status_code=403, detail="Acesso restrito ao proprietário")

@router.post("/recommendations/generate", status_code=202)
async def trigger_recommendation_engine(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    """
    Dispara o job de IA para recalcular recomendações baseadas no histórico.
    """
    # Executa em background para não travar a request
    background_tasks.add_task(run_recommendation_job, str(current_user.id))
    
    return {
        "message": "Motor de IA iniciado. As recomendações aparecerão em breve.",
        "status": "processing"
    }

def run_recommendation_job(company_id: str):
    """Wrapper para rodar o serviço com sua própria sessão de banco"""
    db = SessionLocal()
    try:
        RecommendationService.generate_recommendations(db, company_id)
    except Exception as e:
        print(f"Erro no Job de IA: {e}")
    finally:
        db.close()