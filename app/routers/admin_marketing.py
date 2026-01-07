from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Company, Promotion
from app.schemas import PromotionCreate, PromotionUpdate, PromotionResponse
from app.routers.auth import get_current_user
from app.services.recommendation_service import RecommendationService
from app.services.whatsapp_service import WhatsAppService
from typing import List
from uuid import UUID

router = APIRouter()
whatsapp_service = WhatsAppService()

def require_owner(current_user: any = Depends(get_current_user)):
    if isinstance(current_user, Company):
        return current_user
    raise HTTPException(status_code=403, detail="Acesso restrito ao proprietário")

# --- PROMOÇÕES (CRUD) ---

@router.get("/promotions", response_model=List[PromotionResponse])
def list_promotions(
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    return db.query(Promotion).filter(Promotion.company_id == current_user.id).all()

@router.post("/promotions", response_model=PromotionResponse, status_code=201)
def create_promotion(
    data: PromotionCreate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    # Validar unicidade do código se fornecido
    if data.code:
        exists = db.query(Promotion).filter(
            Promotion.company_id == current_user.id,
            Promotion.code == data.code
        ).first()
        if exists:
            raise HTTPException(400, "Já existe uma promoção com este código.")

    promo = Promotion(
        company_id=current_user.id,
        name=data.name,
        code=data.code,
        discount_type=data.discount_type,
        discount_value=data.discount_value,
        min_order_value=data.min_order_value,
        max_discount_value=data.max_discount_value,
        start_date=data.start_date,
        end_date=data.end_date,
        usage_limit=data.usage_limit
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

@router.patch("/promotions/{promo_id}", response_model=PromotionResponse)
def update_promotion(
    promo_id: UUID,
    data: PromotionUpdate,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    promo = db.query(Promotion).filter(
        Promotion.id == promo_id,
        Promotion.company_id == current_user.id
    ).first()

    if not promo:
        raise HTTPException(404, "Promoção não encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(promo, key, value)

    db.commit()
    db.refresh(promo)
    return promo

@router.delete("/promotions/{promo_id}", status_code=204)
def delete_promotion(
    promo_id: UUID,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    promo = db.query(Promotion).filter(
        Promotion.id == promo_id,
        Promotion.company_id == current_user.id
    ).first()

    if not promo:
        raise HTTPException(404, "Promoção não encontrada")

    db.delete(promo)
    db.commit()
    return None

# --- IA & WHATSAPP (Mantidos) ---

@router.post("/recommendations/generate", status_code=202)
async def trigger_recommendation_engine(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    background_tasks.add_task(run_recommendation_job, str(current_user.id))
    return {
        "message": "Motor de IA iniciado. As recomendações aparecerão em breve.",
        "status": "processing"
    }

@router.get("/whatsapp/status", status_code=200)
async def check_whatsapp_status(
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    status = await whatsapp_service.get_instance_status(current_user)
    return status

@router.post("/whatsapp/test", status_code=200)
async def test_whatsapp_connection(
    db: Session = Depends(get_db),
    current_user: Company = Depends(require_owner)
):
    if not current_user.whatsapp_number:
        raise HTTPException(status_code=400, detail="Configure seu número de WhatsApp primeiro.")

    success = await whatsapp_service.send_test_message(current_user)

    if success:
        return {"message": "Mensagem de teste enviada com sucesso!", "status": "success"}
    else:
        raise HTTPException(status_code=502, detail="Falha ao enviar mensagem. Verifique URL, Instância e Token.")

def run_recommendation_job(company_id: str):
    db = SessionLocal()
    try:
        RecommendationService.generate_recommendations(db, company_id)
    except Exception as e:
        print(f"Erro no Job de IA: {e}")
    finally:
        db.close()