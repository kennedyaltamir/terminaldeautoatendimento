# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 02:30:00
import os

def fix_env():
    print("🔧 Corrigindo encoding do arquivo .env...")
    if not os.path.exists(".env"):
        print("❌ Arquivo .env não encontrado.")
        return

    try:
        # Lê o arquivo tentando detectar encoding problemático
        with open(".env", "rb") as f:
            content = f.read()
        
        # Decodifica ignorando erros e recodifica em UTF-8 limpo
        # Isso remove bytes como 0xe7 se não estiverem em UTF-8
        decoded = content.decode("utf-8", errors="replace")
        
        # Se houver 'ç' literal, garante que seja UTF-8
        with open(".env", "w", encoding="utf-8") as f:
            f.write(decoded)
            
        print("✅ Arquivo .env salvo como UTF-8 puro.")
    except Exception as e:
        print(f"❌ Erro ao processar .env: {e}")

if __name__ == "__main__":
    fix_env()
