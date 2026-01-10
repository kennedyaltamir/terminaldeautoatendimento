import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Company
from app.core.security import get_password_hash

def create_admin():
    db: Session = SessionLocal()
    
    email = "admin@mesaflow.com"
    senha_plana = "123456"
    
    print(f"🔐 Criando/Atualizando usuário admin...")
    print(f"📧 Email: {email}")
    print(f"🔑 Senha: {senha_plana}")

    company = db.query(Company).filter(Company.owner_email == email).first()
    
    if not company:
        # Se não existe, vamos pegar a primeira empresa criada pelo seed ou criar uma nova
        company = db.query(Company).first()
        if not company:
            print("❌ Nenhuma empresa encontrada. Rode o seed.py primeiro.")
            return
        
        print(f"⚠️ Atualizando a empresa '{company.name}' para ser o admin.")
        company.owner_email = email
    
    # Atualiza a senha com o hash seguro
    company.password_hash = get_password_hash(senha_plana)
    db.commit()
    
    print("✅ Senha definida com sucesso!")
    print("👉 Teste o login em: POST /api/auth/token")
    
    db.close()

if __name__ == "__main__":
    create_admin()