# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 02:25:00
import sys
import os
import io
from sqlalchemy import text
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.getcwd())
from app.database import SessionLocal
from app.services.payment_service import PaymentService
from app.models.fintech import PaymentTransaction
REPORT_PATH = "comunication/reports/REPORT_APP_02.md"
def run_idempotency_test():
    """
    APP-02: Prova de Idempotência Financeira (v2 - Passive Validation).
    Valida o bloqueio de duplicidade sem inserir novos dados (Zero-Touch).
    """
    print("💰 Running APP-02: Idempotency Validation (v2)...")
    db = SessionLocal()
    payment_service = PaymentService()
    try:
        # 1. Busca uma transação existente no banco para testar o bloqueio
        print("   [1/2] Searching for existing transaction...")
        existing_tx = db.query(PaymentTransaction).first()
        report_content = ""
        success = False
        if existing_tx:
            print(f"      Found TX: {existing_tx.external_id}. Testing duplicate block...")
            # 2. Tenta registrar a MESMA transação via serviço
            # O método deve retornar False (Idempotência ativa)
            is_new = payment_service.register_transaction_idempotent(
                db, 
                str(existing_tx.company_id), 
                str(existing_tx.order_id), 
                existing_tx.provider, 
                existing_tx.external_id, 
                existing_tx.amount
            )
            success = (is_new is False)
            report_content = (
                f"## Resultado do Teste\n"
                f"- **ID Externo Testado:** `{existing_tx.external_id}`\n"
                f"- **Status Retornado:** `is_new={is_new}`\n"
                f"- **Veredito:** {'✅ Bloqueio de duplicidade funcional.' if success else '❌ Falha: O sistema permitiu duplicata.'}\n"
            )
        else:
            print("   ⚠️  No transactions found in database. Skipping functional test.")
            report_content = (
                "## Resultado do Teste\n"
                "⚠️ **SKIPPED:** Nenhuma transação encontrada no banco para validar a idempotência passivamente.\n"
                "Ação sugerida: Execute o seed de dados ou realize uma venda de teste.\n"
            )
            success = True # Não falha o pipeline por falta de dados, apenas avisa
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("# 💰 Idempotency Validation Report (APP-02)\n\n")
            f.write("## Objetivo\n")
            f.write("Garantir que o serviço de pagamentos bloqueie o re-processamento de IDs externos já existentes.\n\n")
            f.write(report_content)
        print(f"✅ Report: {REPORT_PATH}")
        return 0 if success else 1
    except Exception as e:
        print(f"💥 Error: {e}")
        return 1
    finally:
        db.close()
if __name__ == "__main__":
    sys.exit(run_idempotency_test())
