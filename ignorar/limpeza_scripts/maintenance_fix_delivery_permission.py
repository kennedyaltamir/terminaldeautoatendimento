# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 18:10:00
import requests
import sys
import os
import uuid
from decimal import Decimal
from datetime import datetime

# Adiciona o diretório raiz ao path para importar app.database
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import Company, Employee, Order, OrderStatus, OrderType, Table, TableSession, PaymentStatus
from app.core.security import create_access_token

BASE_URL = "http://localhost:8000/api"
ADMIN_EMAIL = "admin@mesaflow.com"

def fix_and_seed():
    print("🔧 Iniciando Correção de Permissões e Seed de Dados...")
    db = SessionLocal()
    
    try:
        # 1. Diagnóstico e Correção de Permissão (Backend)
        print("\n[1/3] Verificando Usuário Admin...")
        company = db.query(Company).filter(Company.owner_email == ADMIN_EMAIL).first()
        
        if not company:
            print("❌ Empresa admin não encontrada. Rode o seed.py primeiro.")
            return

        print(f"   Empresa: {company.name} (ID: {company.id})")
        print(f"   Role Atual: {company.owner_role}")
        
        # Força role de owner se estiver diferente (embora Company seja sempre owner na lógica atual)
        # O problema do 403 geralmente é na lógica do router.
        # Vamos garantir que o token gerado tenha os escopos corretos.
        
        # 2. Seed de Delivery (Resolver Empty State + Testar 403)
        print("\n[2/3] Criando Pedido de Delivery (Para popular Dashboard)...")
        
        # Verifica se já existe um pedido de delivery pronto
        existing_delivery = db.query(Order).filter(
            Order.company_id == company.id,
            Order.order_type == OrderType.DELIVERY,
            Order.status == OrderStatus.READY
        ).first()

        if not existing_delivery:
            delivery_order = Order(
                company_id=company.id,
                order_type=OrderType.DELIVERY,
                status=OrderStatus.READY, # Status que aparece no painel de despacho
                payment_status=PaymentStatus.PAID,
                customer_name="Cliente Teste Delivery",
                customer_phone="11999999999",
                delivery_address="Av. Paulista, 1000",
                total_amount=Decimal("50.00"),
                created_at=datetime.now()
            )
            db.add(delivery_order)
            db.commit()
            print("   ✅ Pedido de Delivery criado com sucesso.")
        else:
            print("   ℹ️  Pedido de Delivery já existe.")

        # 3. Seed de Mesa (Resolver Empty State do App Garçom)
        print("\n[3/3] Abrindo Mesa (Para popular App Garçom)...")
        table = db.query(Table).filter(Table.company_id == company.id, Table.table_number == 1).first()
        
        if table:
            # Verifica se já tem sessão
            active_session = db.query(TableSession).filter(
                TableSession.table_id == table.id,
                TableSession.is_active == True
            ).first()

            if not active_session:
                session = TableSession(
                    company_id=company.id,
                    table_id=table.id,
                    customer_name="Cliente Mesa 1",
                    session_token=str(uuid.uuid4()),
                    access_pin="1234567890",
                    is_active=True
                )
                db.add(session)
                db.commit()
                print("   ✅ Mesa 1 aberta com sucesso.")
            else:
                print("   ℹ️  Mesa 1 já está ocupada.")
        else:
            print("   ⚠️  Mesa 1 não encontrada.")

        # 4. Validação de Acesso à API (Simulando o Frontend)
        print("\n[4/4] Validando Acesso à API (Teste do 403)...")
        
        # Gera token fresco
        token = create_access_token(data={
            "sub": company.owner_email,
            "role": "owner",
            "account_type": "company",
            "company_id": str(company.id)
        })
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            res = requests.get(f"{BASE_URL}/admin/delivery/orders", headers=headers)
            if res.status_code == 200:
                data = res.json()
                print(f"   ✅ SUCESSO: API retornou 200 OK.")
                print(f"   📦 Pedidos encontrados: {len(data)}")
            else:
                print(f"   ❌ FALHA: API retornou {res.status_code}")
                print(f"   Detalhe: {res.text}")
                print("   👉 Dica: Verifique o arquivo 'app/routers/admin_delivery.py' e a função 'require_delivery_access'.")
        except Exception as e:
            print(f"   ❌ Erro de conexão: {e}")

    except Exception as e:
        print(f"❌ Erro no script: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_and_seed()
