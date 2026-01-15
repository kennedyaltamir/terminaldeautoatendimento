import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Company

def configurar():
    # PERGUNTA O TOKEN NO TERMINAL
    token = input("37cHApuHWF0o1tEst5659G82WNG_4vGpEHUTetiWcSYZEw6LD").strip()
    
    if not token.startswith("APP_USR-"):
        print("❌ Token inválido! Deve começar com APP_USR-")
        return

    db: Session = SessionLocal()
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    
    if not company:
        print("❌ Empresa não encontrada. Rode o seed.py primeiro.")
        return

    company.mp_access_token = token
    company.marketplace_fee_percentage = 1.00 # 1% de comissão para teste
    
    db.commit()
    print(f"✅ Token salvo com sucesso para {company.name}!")
    print("Agora o sistema vai gerar Pix REAIS no Mercado Pago.")

if __name__ == "__main__":
    configurar()