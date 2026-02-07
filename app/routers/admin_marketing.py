# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-07 00:25:00
"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.2.0 (RBAC & Tenant Fix)
 * DNA_ID: MF-ROUTER-MARKETING-V1-2
 * OBJETIVO: Router de Marketing com suporte a RBAC (Gerentes) e resolução de Tenant.
 * CORREÇÃO: 
 *  1. Substitui 'require_owner' por 'require_marketing_access' para permitir gerentes.
 *  2. Implementa 'get_company_id' para evitar erro de UUID vs Int.
 *  3. Ajusta chamadas do WhatsAppService para usar o objeto Company correto.
 */
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Union
from uuid import UUID
from app.database import get_db, SessionLocal
from app.models import Company, Promotion, Employee
from app.schemas import PromotionCreate, PromotionUpdate, PromotionResponse
from app.routers.auth import get_current_user
from app.services.recommendation_service import RecommendationService
from app.services.whatsapp_service import WhatsAppService

router = APIRouter()
whatsapp_service = WhatsAppService()

# --- HELPERS DE SEGURANÇA E CONTEXTO ---

def get_company_id(user: Union[Company, Employee]) -> str:
    """Resolve o ID da empresa (UUID) independente do tipo de usuário."""
    if isinstance(user, Company):
        return str(user.id)
    return str(user.company_id)

def get_company_instance(user: Union[Company, Employee]) -> Company:
    """Retorna a instância da empresa para acesso a configurações (ex: whatsapp)."""
    if isinstance(user, Company):
        return user
    return user.company

def require_marketing_access(current_user: Union[Company, Employee] = Depends(get_current_user)):
    """
    Permite acesso a Proprietários (Company) e Funcionários (Employee) 
    com cargos de gestão (owner, manager, admin).
    """
    if isinstance(current_user, Company):
        return current_user
    
    # Validação de Role para Funcionários
    allowed_roles = ['owner', 'manager', 'admin']
    # Normaliza role para string caso seja Enum
    role = str(current_user.role.value if hasattr(current_user.role, 'value') else current_user.role).lower()
    
    if role in allowed_roles:
        return current_user
        
    raise HTTPException(status_code=403, detail="Acesso restrito a gerentes e proprietários")

# --- PROMOÇÕES (CRUD) ---

@router.get("/promotions", response_model=List[PromotionResponse])
def list_promotions(
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company_id = get_company_id(current_user)
    return db.query(Promotion).filter(Promotion.company_id == company_id).all()

@router.post("/promotions", response_model=PromotionResponse, status_code=201)
def create_promotion(
    data: PromotionCreate,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company_id = get_company_id(current_user)
    
    if data.code:
        exists = db.query(Promotion).filter(
            Promotion.company_id == company_id,
            Promotion.code == data.code
        ).first()
        if exists:
            raise HTTPException(400, "Já existe uma promoção com este código.")
            
    promo = Promotion(
        company_id=company_id,
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
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company_id = get_company_id(current_user)
    promo = db.query(Promotion).filter(
        Promotion.id == promo_id,
        Promotion.company_id == company_id
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
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company_id = get_company_id(current_user)
    promo = db.query(Promotion).filter(
        Promotion.id == promo_id,
        Promotion.company_id == company_id
    ).first()
    
    if not promo:
        raise HTTPException(404, "Promoção não encontrada")
        
    db.delete(promo)
    db.commit()
    return None

# --- IA & WHATSAPP ---

@router.post("/recommendations/generate", status_code=202)
async def trigger_recommendation_engine(
    background_tasks: BackgroundTasks,
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company_id = get_company_id(current_user)
    background_tasks.add_task(run_recommendation_job, str(company_id))
    return {
        "message": "Motor de IA iniciado. As recomendações aparecerão em breve.",
        "status": "processing"
    }

@router.get("/whatsapp/status")
async def check_whatsapp_status(
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company = get_company_instance(current_user)
    try:
        status = await whatsapp_service.get_instance_status(company)
        return status
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}

@router.post("/whatsapp/test", status_code=200)
async def test_whatsapp_connection(
    current_user: Union[Company, Employee] = Depends(require_marketing_access)
):
    company = get_company_instance(current_user)
    
    if not company.whatsapp_number:
        raise HTTPException(status_code=400, detail="Configure seu número de WhatsApp primeiro.")
        
    success = await whatsapp_service.send_test_message(company)
    if success:
        return {"message": "Mensagem de teste enviada com sucesso!", "status": "success"}
    else:
        raise HTTPException(status_code=502, detail="Falha ao enviar mensagem.")

def run_recommendation_job(company_id: str):
    db = SessionLocal()
    try:
        RecommendationService.generate_recommendations(db, company_id)
    except Exception as e:
        print(f"Erro no Job de IA: {e}")
    finally:
        db.close()
