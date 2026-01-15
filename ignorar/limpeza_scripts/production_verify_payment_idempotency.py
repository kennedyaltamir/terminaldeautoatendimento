# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-08 23:30:00
import sys
import os
from decimal import Decimal
import uuid

# Ajuste de path para alcançar a raiz do projeto
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

from app.database import SessionLocal, engine, Base
from app.models import Company, Order, PaymentProvider, PaymentTransaction
from app.services.payment_service import PaymentService

def verify_idempotency():
    print("🔍 Verificando TASK-FIN-02: Idempotência de Pagamento...")

    # Garante que as tabelas existem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    service = PaymentService()

    temp_company = None
    temp_order = None

    try:
        # 1. Setup - Criar registros reais para satisfazer as Foreign Keys (Integridade Referencial)
        print("🏗️  Preparando ambiente de teste (Registros temporários)...")
        
        # Criar Empresa Temporária
        temp_company = Company(
            name="Idempotency Test Corp",
            slug=f"test-idemp-{uuid.uuid4().hex[:6]}",
            owner_email=f"test-{uuid.uuid4().hex[:6]}@mesaflow.com"
        )
        db.add(temp_company)
        db.flush() # Gera o ID
        
        # Criar Pedido Temporário vinculado à empresa
        temp_order = Order(
            company_id=temp_company.id,
            customer_name="Test User",
            total_amount=Decimal("50.00")
        )
        db.add(temp_order)
        db.commit()
        
        cid = temp_company.id
        oid = temp_order.id
        external_tx_id = f"test_tx_{uuid.uuid4().hex[:8]}"

        # 2. Primeira Chamada (Deve retornar True)
        print(f"🧪 Testando inserção da transação {external_tx_id}...")
        res1 = service.register_transaction_idempotent(
            db, str(cid), str(oid), PaymentProvider.MERCADO_PAGO, external_tx_id, Decimal("50.00")
        )
        db.commit()
        
        if res1 is True:
            print("✅ Primeira chamada aceita.")
        else:
            print("❌ Falha: Primeira chamada deveria ser True.")
            sys.exit(1)

        # 3. Segunda Chamada (Deve retornar False)
        print("🧪 Testando duplicidade (mesmo provider e external_id)...")
        res2 = service.register_transaction_idempotent(
            db, str(cid), str(oid), PaymentProvider.MERCADO_PAGO, external_tx_id, Decimal("50.00")
        )
        
        if res2 is False:
            print("✅ Segunda chamada bloqueada corretamente.")
        else:
            print("❌ FALHA CRÍTICA: O sistema permitiu processar a mesma transação duas vezes!")
            sys.exit(1)

        # 4. Limpeza
        print("🧹 Limpando registros de teste...")
        db.query(PaymentTransaction).filter(PaymentTransaction.external_id == external_tx_id).delete()
        db.delete(temp_order)
        db.delete(temp_company)
        db.commit()

    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        # Tenta limpar em caso de erro para não sujar o banco de produção
        try:
            db.rollback()
            if temp_order: db.delete(temp_order)
            if temp_company: db.delete(temp_company)
            db.commit()
        except:
            pass
        sys.exit(1)
    finally:
        db.close()

    print("\n🏆 Idempotency Check Passed: Double-payment blocked.")
    sys.exit(0)

if __name__ == "__main__":
    verify_idempotency()
