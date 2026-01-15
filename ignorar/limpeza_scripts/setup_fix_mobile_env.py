import os
from pathlib import Path

def fix_mobile_env():
    print("🔧 Configurando ambiente Mobile...")
    
    root_dir = Path.cwd()
    mobile_dir = root_dir / "mobile"
    env_file = mobile_dir / ".env"
    
    # Configuração para Emulador (com adb reverse)
    # Usamos localhost porque o script de doutor já garantiu o mapeamento de portas
    content = (
        "APP_ENV=development\n"
        "API_URL=http://localhost:8000/api\n"
        "GOOGLE_CLIENT_ID=\n"
    )
    
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Arquivo criado: {env_file}")
        print("   Conteúdo:")
        print(content)
        print("\n⚠️  IMPORTANTE: Como as variáveis mudaram, você DEVE recompilar o APK.")
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")

if __name__ == "__main__":
    fix_mobile_env()
