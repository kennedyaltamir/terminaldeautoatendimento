# DOMAIN: DEVOPS_SCRIPTS
import sys
import os
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import Base
from app.models import GlobalUser, GlobalWallet

def verify():
    print("🔍 Verificando TASK-NET-01: Arquitetura MesaFlow Passport...")

    # Configuração de Banco em Memória para Teste
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 1. Criar Tabelas
    print("🏗️  Criando esquema de banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        sys.exit(1)

    db = SessionLocal()

    try:
        # 2. Inserir Global User
        print("🧪 Teste 1: Inserção de Global User...")
        phone = "5511999998888"
        user = GlobalUser(
            phone=phone,
            name="Passport User",
            email="passport@test.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        if user.id:
            print(f"✅ Usuário Global criado: {user.id}")
        else:
            print("❌ Falha ao criar usuário global.")
            sys.exit(1)

        # 3. Inserir Global Wallet
        print("🧪 Teste 2: Criação de Global Wallet...")
        wallet = GlobalWallet(
            global_user_id=user.id,
            balance=100.00
        )
        db.add(wallet)
        db.commit()
        db.refresh(wallet)

        if wallet.id and wallet.global_user_id == user.id:
            print(f"✅ Carteira Global criada e vinculada: {wallet.id}")
        else:
            print("❌ Falha ao criar carteira global.")
            sys.exit(1)

        # 4. Verificar Relacionamento
        print("🧪 Teste 3: Verificação de Relacionamento...")
        db.refresh(user)
        if len(user.wallets) > 0 and user.wallets[0].id == wallet.id:
            print("✅ Relacionamento User -> Wallet validado.")
        else:
            print("❌ Falha no relacionamento ORM.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        sys.exit(1)
    finally:
        db.close()

    print("\n🏆 TASK-NET-01: VALIDAÇÃO CONCLUÍDA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
