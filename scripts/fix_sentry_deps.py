import subprocess
import os
import sys

def install_sentry():
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Pasta 'frontend' não encontrada.")
        return

    print("📦 Instalando Sentry SDK no Frontend...")
    
    cmd = ["npm", "install", "@sentry/nextjs"]
    
    try:
        subprocess.check_call(cmd, cwd=frontend_dir, shell=True)
        print("✅ Dependências do Sentry instaladas!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar: {e}")

    print("\n📦 Instalando Sentry SDK no Backend...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sentry-sdk[fastapi]"])
        print("✅ Backend Sentry instalado!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar backend: {e}")

if __name__ == "__main__":
    install_sentry()