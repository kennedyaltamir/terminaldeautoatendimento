import sys
import os
from sqlalchemy import text

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def fix_enum_data():
    print("💳 Corrigindo dados de PaymentProvider para UPPERCASE...")
    
    commands = [
        "UPDATE companies SET payment_provider = 'NONE' WHERE payment_provider = 'none';",
        "UPDATE companies SET payment_provider = 'MERCADO_PAGO' WHERE payment_provider = 'mercadopago';",
        "UPDATE companies SET payment_provider = 'STRIPE' WHERE payment_provider = 'stripe';",
        "UPDATE companies SET payment_provider = 'EFI' WHERE payment_provider = 'efi';",
        "UPDATE companies SET payment_provider = 'PAGARME' WHERE payment_provider = 'pagarme';"
    ]

    with engine.connect() as conn:
        for cmd in commands:
            try:
                res = conn.execute(text(cmd))
                print(f"✅ {cmd} ({res.rowcount} linhas afetadas)")
            except Exception as e:
                print(f"⚠️ Erro: {e}")
        conn.commit()
    
    print("\n🎉 Dados sincronizados com o novo padrão do Model!")

if __name__ == "__main__":
    fix_enum_data()