# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:20:00
import sys
import os
import io
import uuid

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())
from app.database import SessionLocal
from app.services.ledger_service import LedgerService
from app.models.company import Company

def test_financial_integrity():
    db = SessionLocal()
    print("💰 Preparando ambiente para teste de Ledger L7...")
    try:
        temp_company = Company(
            name="Test Ledger Corp",
            slug=f"test-ledger-{uuid.uuid4().hex[:4]}",
            owner_email=f"ledger-{uuid.uuid4().hex[:4]}@test.com"
        )
        db.add(temp_company)
        db.commit()
        db.refresh(temp_company)
        company_id = str(temp_company.id)
        
        print(f"✅ Empresa de teste criada: {company_id}")
        
        e1 = LedgerService.create_entry(db, company_id, 1000, "CREDIT", "test", "ref1", "Venda 1")
        e2 = LedgerService.create_entry(db, company_id, 300, "DEBIT", "test", "ref2", "Taxa 1")
        db.commit()
        
        is_ok, msg = LedgerService.verify_chain(db, company_id)
        print(f"🔍 Auditoria: {msg}")
        
        if is_ok and e2.balance_after == 700:
            print("✨ SUCESSO: Integridade L7 validada.")
            return True
        else:
            print("❌ FALHA: Saldo ou Hash incorreto.")
            return False
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(0 if test_financial_integrity() else 1)

