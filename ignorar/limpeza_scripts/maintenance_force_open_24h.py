# DOMAIN: DEVOPS_SCRIPTS
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import Company

def force_open():
    print("🔓 Forçando abertura da loja (Modo 24h)...")
    
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        
        if not company:
            print("❌ Empresa 'hamburgueria-ze' não encontrada.")
            return

        # Definir horários como NULL faz o sistema entender que é 24h
        company.opens_at = None
        company.closes_at = None
        
        db.commit()
        print(f"✅ Sucesso! A loja '{company.name}' agora está aberta 24h.")
        print("👉 Tente criar o pedido novamente.")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    force_open()
