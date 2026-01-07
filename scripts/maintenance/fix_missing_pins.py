import sys
import os
import random
import string
from sqlalchemy import func

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models import TableSession

def generate_secure_pin(length: int = 10) -> str:
    return ''.join(random.choices(string.digits, k=length))

def fix_pins():
    print("🔧 Corrigindo sessões sem Token de Acesso...")
    db = SessionLocal()
    
    try:
        # Busca sessões ativas que estão com o PIN nulo ou com o padrão antigo de 4 dígitos
        sessions = db.query(TableSession).filter(
            TableSession.is_active == True,
            (TableSession.access_pin == None) | (func.length(TableSession.access_pin) < 10)
        ).all()

        if not sessions:
            print("✨ Nenhuma sessão precisando de correção.")
            return

        for session in sessions:
            new_pin = generate_secure_pin(10)
            session.access_pin = new_pin
            print(f"✅ Mesa {session.table_id}: Token gerado -> {new_pin}")
        
        db.commit()
        print(f"\n🎉 Sucesso! {len(sessions)} tokens corrigidos.")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_pins()
