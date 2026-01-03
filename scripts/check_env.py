import os
from dotenv import load_dotenv

def check():
    print("🔍 Verificando variáveis de ambiente...")
    
    # Carrega do arquivo .env
    load_dotenv()
    
    db_url = os.getenv("DATABASE_URL")
    
    print(f"   DATABASE_URL encontrada: '{db_url}'")
    
    if db_url is None:
        print("⚠️  A variável DATABASE_URL não existe. O sistema usará o padrão.")
    elif db_url == "":
        print("❌ A variável DATABASE_URL existe mas está VAZIA. Isso causa erro no SQLAlchemy.")
        print("👉 Solução: Remova a linha do .env ou preencha com a URL correta.")
    else:
        print("✅ DATABASE_URL parece válida.")

if __name__ == "__main__":
    check()