# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:32:00
import sys
import os
from sqlalchemy import text

# Adiciona a raiz ao path para permitir importações do app
sys.path.append(os.getcwd())

try:
    from app.database import SessionLocal
    from app.models import Company, Order, OrderItem
except ImportError:
    print("❌ Erro: Módulos do sistema não encontrados. Execute o script na raiz do projeto.")
    sys.exit(1)

def clear_orders(slug: str):
    print(f"🧹 Iniciando limpeza de pedidos para o restaurante: {slug}")
    db = SessionLocal()
    
    try:
        # 1. Localizar a Empresa pelo Slug
        company = db.query(Company).filter(Company.slug == slug).first()
        if not company:
            print(f"❌ Erro: Empresa com slug '{slug}' não encontrada.")
            return

        company_id = company.id
        print(f"   ID da Empresa: {company_id}")

        # 🛡️ BYPASS RLS PARA MANUTENÇÃO (Executando como Superuser/Admin)
        db.execute(text("SET row_security = off"))

        # 2. Deletar Itens dos Pedidos primeiro (Integridade Referencial)
        print("   [1/2] Removendo itens dos pedidos...")
        db.query(OrderItem).filter(
            OrderItem.order_id.in_(
                db.query(Order.id).filter(Order.company_id == company_id)
            )
        ).delete(synchronize_session=False)

        # 3. Deletar os Pedidos
        print("   [2/2] Removendo pedidos da base...")
        deleted_count = db.query(Order).filter(Order.company_id == company_id).delete(synchronize_session=False)

        db.commit()
        print(f"✅ Sucesso! {deleted_count} pedidos foram removidos.")
        print("👉 A tela da cozinha/balcão deve estar limpa agora.")

    except Exception as e:
        db.rollback()
        print(f"💥 Erro crítico durante a limpeza: {e}")
    finally:
        # Reativa RLS por segurança
        db.execute(text("SET row_security = on"))
        db.close()

if __name__ == "__main__":
    # Slug fixo conforme solicitado na URL
    TARGET_SLUG = "hamburgueria-ze"
    clear_orders(TARGET_SLUG)

