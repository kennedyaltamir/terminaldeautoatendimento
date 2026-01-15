import secrets
import base64

def generate_keys():
    print("🔐 Gerador de Segredos para Produção (MesaFlow)\n")
    
    # 1. SECRET_KEY (JWT)
    # Gera 64 bytes aleatórios e codifica em hex
    secret_key = secrets.token_hex(32)
    print(f"🔑 SECRET_KEY (Copie para o Render/Vercel):")
    print(f"{secret_key}\n")
    
    # 2. Senha de Admin Inicial (Forte)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    admin_pass = "".join(secrets.choice(alphabet) for i in range(16))
    print(f"👤 Senha Sugerida para Admin Inicial:")
    print(f"{admin_pass}\n")
    
    # 3. Webhook Secrets (Simulação de formato)
    stripe_wh = "whsec_" + secrets.token_hex(24)
    print(f"💳 Exemplo de formato STRIPE_WEBHOOK_SECRET:")
    print(f"{stripe_wh}\n")

    print("⚠️  IMPORTANTE: Salve estes valores no seu gerenciador de senhas ou nas variáveis de ambiente da nuvem.")
    print("   NUNCA commite este output ou arquivos .env reais no Git.")

if __name__ == "__main__":
    generate_keys()
