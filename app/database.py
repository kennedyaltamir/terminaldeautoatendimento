import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Lógica robusta para URL de conexão
env_url = os.getenv("DATABASE_URL")

# 1. Sanitização Básica
if env_url:
    env_url = env_url.strip().strip('"').strip("'")

    # 2. CORREÇÃO CRÍTICA: SQLAlchemy exige 'postgresql://' em vez de 'postgres://'
    if env_url.startswith("postgres://"):
        env_url = env_url.replace("postgres://", "postgresql://", 1)

if not env_url:
    # Fallback para desenvolvimento local
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mesaflow_db"
else:
    SQLALCHEMY_DATABASE_URL = env_url

# Criação da Engine
try:
    # pool_pre_ping=True ajuda a reconectar se a conexão cair (comum em nuvem/Neon)
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
except Exception as e:
    print(f"❌ Erro fatal ao conectar no banco: {e}")
    # Não printamos a URL completa por segurança, apenas o protocolo detectado
    print(f"   Protocolo utilizado: {SQLALCHEMY_DATABASE_URL.split('://')[0] if '://' in SQLALCHEMY_DATABASE_URL else 'Nenhum'}")
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
