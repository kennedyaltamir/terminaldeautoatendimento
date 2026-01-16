# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 15:20:00
import os
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

# Força o carregamento do .env com encoding explícito para evitar byte 0xe7 no Windows
load_dotenv(encoding='utf-8')

def sanitize_db_url(url: str) -> str:
    if not url:
        return "postgresql://postgres:postgres@localhost:5432/mesaflow_db"
    
    # Limpeza de caracteres invisíveis, aspas e espaços
    url = url.strip().strip('"').strip("'")
    
    # Correção de protocolo para SQLAlchemy 1.4+
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        
    return url

# Obtém e sanitiza a URL
raw_url = os.getenv("DATABASE_URL", "")
DATABASE_URL = sanitize_db_url(raw_url)

# Configuração do Engine com Hardening para Windows
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=10,
    max_overflow=20,
    # Força o encoding da conexão para evitar erros de handshake no Windows
    connect_args={
        "client_encoding": "utf8",
        "application_name": "MesaFlow_Backend"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # Garante que a conexão respeita o RLS na sessão atual
        db.execute(text("SET row_security = on"))
        yield db
    finally:
        db.close()

def set_tenant(db: Session, company_id: str):
    """
    Define a variável de sessão do PostgreSQL para o Tenant atual.
    """
    try:
        if not company_id:
            db.execute(text("SET LOCAL app.current_company_id = ''"))
            return
        # Sanitização básica contra SQL Injection na variável de sessão
        clean_id = re.sub(r"[^a-f0-9\-]", "", str(company_id).lower())
        db.execute(text(f"SET LOCAL app.current_company_id = '{clean_id}'"))
    except Exception as e:
        db.execute(text("SET LOCAL app.current_company_id = ''"))
        raise e

