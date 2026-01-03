import subprocess
import os
import sys

def setup_e2e():
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Pasta 'frontend' não encontrada.")
        return

    print("🎭 Configurando Playwright para testes E2E...")

    # 1. Instalar dependências do Playwright no package.json
    print("📦 Instalando pacotes npm...")
    try:
        subprocess.check_call(["npm", "install"], cwd=frontend_dir, shell=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências npm.")
        return

    # 2. Instalar binários dos navegadores
    print("🌍 Baixando navegadores do Playwright...")
    try:
        subprocess.check_call(["npx", "playwright", "install", "chromium"], cwd=frontend_dir, shell=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao baixar navegadores.")
        return

    print("\n✅ Ambiente E2E configurado!")
    print("👉 Para rodar o teste: cd frontend && npm run test:e2e")

if __name__ == "__main__":
    setup_e2e()