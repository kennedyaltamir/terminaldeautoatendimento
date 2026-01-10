# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-10 02:15:00
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

load_dotenv()

# Lógica robusta para URL de conexão com sanitização de prefixos CLI e protocolos
raw_url = os.getenv("DATABASE_URL")

def sanitize_db_url(url: str) -> str:
    if not url:
        # Fallback para desenvolvimento local
        return "postgresql://postgres:postgres@localhost:5432/mesaflow_db"
    
    # 1. Limpeza de espaços e aspas (comum no Windows/PowerShell)
    url = url.strip().strip('"').strip("'")
    
    # 2. Remoção de prefixos de CLI (ex: 'psql ' que causou o erro anterior)
    if url.lower().startswith("psql "):
        url = url[5:].strip()
        
    # 3. CORREÇÃO CRÍTICA: SQLAlchemy exige 'postgresql://' em vez de 'postgres://'
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        
    return url

SQLALCHEMY_DATABASE_URL = sanitize_db_url(raw_url)

# 4. Validação de Pooling para Neon (Produção)
if "neon.tech" in SQLALCHEMY_DATABASE_URL and "-pooler" not in SQLALCHEMY_DATABASE_URL:
    print("⚠️  AVISO DE INFRAESTRUTURA: Conexão direta com Neon detectada.")
    print("   Recomendação: Use a string '-pooler' para evitar exaustão de conexões.")

# Criação da Engine com Configuração de Pool Blindada
try:
    connect_args = {}
    # Configuração de Pool para PostgreSQL (Produção/Staging)
    pool_config = {
        "pool_size": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_pre_ping": True,
        "pool_recycle": 1800
    }

    if "sqlite" in SQLALCHEMY_DATABASE_URL:
        connect_args = {"check_same_thread": False}
        pool_config = {}

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args=connect_args,
        **pool_config
    )
    
    # 5. TESTE DE CONEXÃO IMEDIATO (Fail-Fast)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        
except Exception as e:
    print(f"❌ Erro fatal ao conectar no banco: {str(e)}")
    # Mostra apenas o host para não vazar senha no log
    host_info = SQLALCHEMY_DATABASE_URL.split('@')[-1] if '@' in SQLALCHEMY_DATABASE_URL else "N/A"
    print(f"   Tentativa de conexão em: {host_info}")
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_tenant(db: Session, company_id: str):
    """
    Configura a variável de sessão do PostgreSQL para RLS.
    """
    try:
        if not company_id:
            return

        # Sanitização básica
        clean_id = str(company_id).replace("'", "").replace(";", "")

        if db.bind.dialect.name == 'sqlite':
            return

        db.execute(text(f"SET LOCAL app.current_company_id = '{clean_id}'"))

    except Exception as e:
        print(f"⚠️ Falha ao definir tenant context: {e}")
