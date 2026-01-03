import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Lógica robusta para URL de conexão
env_url = os.getenv("DATABASE_URL")

# Sanitização: Remove espaços e aspas extras que podem vir do .env
if env_url:
    env_url = env_url.strip().strip('"').strip("'")

if not env_url:
    # Fallback para desenvolvimento local se não houver variável
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mesaflow_db"
else:
    SQLALCHEMY_DATABASE_URL = env_url

# Criação da Engine
try:
    # pool_pre_ping=True ajuda a reconectar se a conexão cair (comum em nuvem/Neon)
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
except Exception as e:
    print(f"❌ Erro fatal ao conectar no banco: {e}")
    print(f"   URL Tentada: {SQLALCHEMY_DATABASE_URL}")
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()