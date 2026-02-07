# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-07 00:30:00
"""
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.3.0 (Tenant ID Fix)
 * DNA_ID: MF-ROUTER-AUDIT-V1-3
 * OBJETIVO: Router de Auditoria e Financeiro com resolução robusta de Tenant.
 * CORREÇÃO: Implementa 'get_company_id' para evitar erro de UUID vs Int em endpoints financeiros.
 */
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Union
from app.database import get_db
from app.routers.auth import get_current_user
from app.services.reconciliation_service import ReconciliationService
from app.services.ledger_service import LedgerService
from app.models.company import Company
from app.models.auth import Employee
from app.models.fintech import FinancialLedger
from app.models.system import AuditLog
from app.schemas.system import AuditLogResponse

router = APIRouter()

# --- HELPER: RESOLUÇÃO DE TENANT ---
def get_company_id(user: Union[Company, Employee]) -> str:
    """
    Resolve o ID da empresa (UUID).
    Se for Employee, usa user.company_id.
    Se for Company (Owner), usa user.id.
    """
    if isinstance(user, Company):
        return str(user.id)
    return str(user.company_id)

# --- GERAL ---

@router.get("", response_model=List[AuditLogResponse])
def get_audit_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """
    Retorna os logs de auditoria do sistema para a empresa atual.
    """
    company_id = get_company_id(current_user)
    return db.query(AuditLog)\
        .filter(AuditLog.company_id == company_id)\
        .order_by(AuditLog.created_at.desc())\
        .limit(limit)\
        .all()

# --- FINANCEIRO ---

@router.get("/financial/reconciliation")
async def get_reconciliation_report(
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    return await ReconciliationService.reconcile_company(db, company_id)

@router.get("/financial/ledger")
async def get_ledger_history(
    limit: int = 50, 
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    entries = db.query(FinancialLedger)\
        .filter(FinancialLedger.company_id == company_id)\
        .order_by(FinancialLedger.sequence_id.desc())\
        .limit(limit)\
        .all()
    return entries

@router.get("/financial/verify-integrity")
async def verify_ledger_integrity(
    db: Session = Depends(get_db), 
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    company_id = get_company_id(current_user)
    is_ok, message = LedgerService.verify_chain(db, company_id)
    return {"is_integral": is_ok, "message": message}

@router.post("/financial/fix-orphan")
async def fix_orphan_transaction(
    external_id: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: Union[Company, Employee] = Depends(get_current_user)
):
    """
    Cria uma entrada no Ledger para uma transação que existe no Gateway mas não no sistema.
    """
    company_id = get_company_id(current_user)
    
    # 1. Re-valida se a transação realmente existe no gateway e é órfã
    report = await ReconciliationService.reconcile_company(db, company_id)
    orphan = next((o for o in report["orphans"] if o["external_id"] == external_id), None)
    
    if not orphan:
        raise HTTPException(status_code=404, detail="Transação órfã não encontrada ou já conciliada.")
    
    # 2. Cria a entrada corretiva no Ledger
    entry = LedgerService.create_entry(
        db, 
        company_id, 
        orphan["amount_cents"], 
        "CREDIT", 
        "payment", 
        external_id, 
        f"Conciliação Automática: {external_id}"
    )
    db.commit()
    return {"status": "fixed", "sequence_id": entry.sequence_id}
