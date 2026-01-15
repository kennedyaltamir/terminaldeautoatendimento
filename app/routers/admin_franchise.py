
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company
from app.routers.auth import get_current_user
from app.services.franchise_service import FranchiseService

router = APIRouter()

@router.get("/dashboard")
def get_franchise_dashboard(
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    if not isinstance(current_user, Company):
        raise HTTPException(status_code=403, detail="Acesso restrito")
    
    data = FranchiseService.get_network_summary(db, current_user.owner_email)
    avg_margin = (data["total_profit"] / data["total_revenue"] * 100) if data["total_revenue"] > 0 else 0
    
    return {
        "total_revenue": data["total_revenue"],
        "total_profit": data["total_profit"],
        "avg_margin": avg_margin,
        "total_orders": data["total_orders"],
        "stores": data["stores"]
    }

