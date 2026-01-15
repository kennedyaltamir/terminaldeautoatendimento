
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 00:50:00
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.fintech import FinancialLedger

class LedgerService:
    """
    Motor de Integridade Financeira L7.
    Encadeamento de transações isolado por Tenant com Flush forçado.
    """
    
    @staticmethod
    def create_entry(db: Session, company_id: str, amount: int, entry_type: str, 
                     category: str, reference_id: str, description: str):
        # 1. Forçar sincronização da sessão para garantir que registros pendentes
        # sejam processados e visíveis para a query abaixo.
        db.flush()

        # 2. Obter a última entrada DAQUELA EMPRESA para encadeamento
        last_entry = db.query(FinancialLedger).filter(
            FinancialLedger.company_id == company_id
        ).order_by(desc(FinancialLedger.sequence_id)).first()
        
        prev_hash = last_entry.integrity_hash if last_entry else "GENESIS"
        current_balance = last_entry.balance_after if last_entry else 0
        
        if entry_type == "CREDIT":
            new_balance = current_balance + amount
        else:
            new_balance = current_balance - amount
            
        # 3. Gerar Hash de Integridade (Chain-link)
        payload = f"{prev_hash}|{company_id}|{amount}|{entry_type}|{new_balance}|{reference_id}"
        integrity_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        entry = FinancialLedger(
            company_id=company_id,
            entry_type=entry_type,
            amount=amount,
            balance_after=new_balance,
            category=category,
            reference_id=reference_id,
            description=description,
            integrity_hash=integrity_hash
        )
        
        db.add(entry)
        # 4. Flush final para garantir que o sequence_id seja gerado pelo DB imediatamente
        db.flush()
        return entry

    @staticmethod
    def verify_chain(db: Session, company_id: str):
        """Verifica a integridade da corrente de uma empresa específica."""
        # Garante que tudo foi para o banco antes de verificar
        db.flush()
        
        entries = db.query(FinancialLedger).filter(
            FinancialLedger.company_id == company_id
        ).order_by(FinancialLedger.sequence_id).all()
        
        if not entries:
            return True, "LEDGER VAZIO"

        prev_hash = "GENESIS"
        for entry in entries:
            payload = f"{prev_hash}|{entry.company_id}|{entry.amount}|{entry.entry_type}|{entry.balance_after}|{entry.reference_id}"
            expected_hash = hashlib.sha256(payload.encode()).hexdigest()
            
            if entry.integrity_hash != expected_hash:
                return False, f"VIOLAÇÃO NA SEQUÊNCIA {entry.sequence_id} (Hash Mismatch)"
            
            prev_hash = entry.integrity_hash
            
        return True, "INTEGRIDADE CONFIRMADA"

