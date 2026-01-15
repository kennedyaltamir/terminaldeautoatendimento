
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 10:45:00
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.routers.auth import get_current_user
from app.services.reconciliation_service import ReconciliationService
from app.services.ledger_service import LedgerService
from app.models.company import Company
from app.models.fintech import FinancialLedger
from app.models.system import AuditLog
from app.schemas.system import AuditLogResponse

router = APIRouter()

# --- GERAL ---

@router.get("", response_model=List[AuditLogResponse])
def get_audit_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: any = Depends(get_current_user)
):
    """
    Retorna os logs de auditoria do sistema para a empresa atual.
    """
    # Determina o ID da empresa baseado no tipo de usuário (Company ou Employee)
    company_id = current_user.id if isinstance(current_user, Company) else current_user.company_id
    
    return db.query(AuditLog)\
        .filter(AuditLog.company_id == company_id)\
        .order_by(AuditLog.created_at.desc())\
        .limit(limit)\
        .all()

# --- FINANCEIRO ---

@router.get("/financial/reconciliation")
async def get_reconciliation_report(db: Session = Depends(get_db), current_user: Company = Depends(get_current_user)):
    return await ReconciliationService.reconcile_company(db, str(current_user.id))

@router.get("/financial/ledger")
async def get_ledger_history(limit: int = 50, db: Session = Depends(get_db), current_user: Company = Depends(get_current_user)):
    entries = db.query(FinancialLedger).filter(FinancialLedger.company_id == current_user.id).order_by(FinancialLedger.sequence_id.desc()).limit(limit).all()
    return entries

@router.get("/financial/verify-integrity")
async def verify_ledger_integrity(db: Session = Depends(get_db), current_user: Company = Depends(get_current_user)):
    is_ok, message = LedgerService.verify_chain(db, str(current_user.id))
    return {"is_integral": is_ok, "message": message}

@router.post("/financial/fix-orphan")
async def fix_orphan_transaction(
    external_id: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: Company = Depends(get_current_user)
):
    """
    Cria uma entrada no Ledger para uma transação que existe no Gateway mas não no sistema.
    """
    # 1. Re-valida se a transação realmente existe no gateway e é órfã
    report = await ReconciliationService.reconcile_company(db, str(current_user.id))
    orphan = next((o for o in report["orphans"] if o["external_id"] == external_id), None)
    
    if not orphan:
        raise HTTPException(status_code=404, detail="Transação órfã não encontrada ou já conciliada.")
    
    # 2. Cria a entrada corretiva no Ledger
    entry = LedgerService.create_entry(
        db, 
        str(current_user.id), 
        orphan["amount_cents"], 
        "CREDIT", 
        "payment", 
        external_id, 
        f"Conciliação Automática: {external_id}"
    )
    db.commit()
    return {"status": "fixed", "sequence_id": entry.sequence_id}

