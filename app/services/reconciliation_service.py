
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 01:55:00
from sqlalchemy.orm import Session
from app.models.fintech import FinancialLedger
from app.services.payment.factory import PaymentFactory
from app.models.company import Company
import logging
logger = logging.getLogger("Reconciliation")
class ReconciliationService:
    """
    Serviço de Conciliação Financeira L7.
    Cruza dados do Ledger Interno com o extrato real do Gateway.
    """
    @staticmethod
    async def reconcile_company(db: Session, company_id: str):
        company = db.query(Company).filter(Company.id == company_id).first()
        # Guard Clause: Verifica se a empresa tem um provedor ativo
        if not company or not company.payment_provider or str(company.payment_provider).lower() == "none":
            return {"status": "skipped", "reason": "No active payment provider"}
        try:
            # 1. Instanciar Provedor via Factory
            provider = PaymentFactory.get_provider(company.payment_provider)
            if not provider:
                return {"status": "skipped", "reason": "Provider implementation missing"}
            # 2. Buscar histórico externo (Gateway)
            external_txs = await provider.get_transaction_history(company)
            # 3. Buscar dados internos (Ledger)
            internal_entries = db.query(FinancialLedger).filter(
                FinancialLedger.company_id == company_id,
                FinancialLedger.category == "payment"
            ).all()
            internal_map = {e.reference_id: e for e in internal_entries}
            report = {
                "status": "success",
                "matched": [], 
                "orphans": [], 
                "ghosts": [], 
                "mismatches": []
            }
            for ext in external_txs:
                ext_id = ext["external_id"]
                if ext_id in internal_map:
                    int_entry = internal_map[ext_id]
                    if int_entry.amount == ext["amount_cents"]:
                        report["matched"].append(ext_id)
                    else:
                        report["mismatches"].append({
                            "id": ext_id, 
                            "expected_gateway": ext["amount_cents"], 
                            "found_ledger": int_entry.amount
                        })
                    del internal_map[ext_id]
                else:
                    if ext["status"] == "approved":
                        report["orphans"].append(ext)
            report["ghosts"] = list(internal_map.keys())
            return report
        except Exception as e:
            logger.error(f"Erro na conciliação da empresa {company_id}: {str(e)}")
            return {"status": "error", "reason": str(e)}
