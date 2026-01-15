# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 02:40:00
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
load_dotenv()

def sanitize_db_url(url: str) -> str:
    if not url:
        return "postgresql://postgres:postgres@localhost:5432/mesaflow_db"
    # Limpeza agressiva de caracteres invisíveis e aspas
    url = url.strip().strip('"').strip("'")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

# FIX: Força a leitura do DATABASE_URL como string UTF-8
DATABASE_URL = sanitize_db_url(os.getenv("DATABASE_URL", ""))

engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=10,
    max_overflow=20,
    # Força o encoding da conexão para evitar erros de byte 0xe7 no Windows
    connect_args={"client_encoding": "utf8"}
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
        clean_id = str(company_id).replace("'", "").replace(";", "")
        db.execute(text(f"SET LOCAL app.current_company_id = '{clean_id}'"))
    except Exception as e:
        db.execute(text("SET LOCAL app.current_company_id = ''"))
        raise e
