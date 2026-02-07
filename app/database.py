# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-02-05 12:50:00
# DESCRIPTION: Database Core - Secure Configuration (No Hardcoded Secrets).
import os
import re
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

# 1. Carrega o .env da raiz
load_dotenv()

def get_url():
    # Tenta obter do ambiente (Render/Neon injetam isso automaticamente)
    url = os.getenv("DATABASE_URL", "")
    
    # 🛡️ HARDENING: Se não houver URL, falha explicitamente em produção.
    # Em dev local, você deve ter o .env configurado.
    if not url:
        # Fallback APENAS para SQLite em memória se for teste, nunca credencial real
        if os.getenv("TEST_MODE") == "true":
            return "sqlite:///:memory:"
        
        print("🚨 ERRO CRÍTICO: DATABASE_URL não encontrada nas variáveis de ambiente.")
        # Retorna string vazia para ser tratada no try/except abaixo
        return ""

    # Limpeza de aspas e espaços
    url = url.strip().replace('"', '').replace("'", "")
    
    # Normaliza protocolo para SQLAlchemy (Postgres requer postgresql://)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    return url

DATABASE_URL = get_url()

engine = None
try:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL vazia.")

    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        # connect_args={"client_encoding": "utf8"} # Removido se causar conflito com alguns drivers, reativar se necessário
    )
except Exception as e:
    print(f"\033[91m[DATABASE_FATAL] Erro ao configurar motor: {e}\033[0m")
    # Não matamos o processo aqui para permitir que scripts de diagnóstico rodem,
    # mas a aplicação principal falhará ao tentar conectar.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    if engine is None:
        raise Exception("Banco de dados não configurado corretamente (Engine is None).")
    db = SessionLocal()
    try:
        # Tenta configurar RLS se suportado, ou ignora silenciosamente em SQLite
        if "postgresql" in DATABASE_URL:
            db.execute(text("SET row_security = on"))
        yield db
    finally:
        db.close()

def set_tenant(db: Session, company_id: str):
    if "postgresql" not in DATABASE_URL:
        return
    if not company_id:
        db.execute(text("SET LOCAL app.current_company_id = ''"))
        return
    clean_id = re.sub(r"[^a-f0-9\-]", "", str(company_id).lower())
    db.execute(text(f"SET LOCAL app.current_company_id = '{clean_id}'"))
