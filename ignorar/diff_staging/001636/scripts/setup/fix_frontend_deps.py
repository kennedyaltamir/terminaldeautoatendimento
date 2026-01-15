# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 00:25:00
import subprocess
import sys
import os
import io

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fix():
    print("🔧 Instalando dependências do Frontend (Sentry & Vitest)...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    # Force install of missing deps
    # Usamos --no-audit para ser mais rápido
    cmd = "npm install @sentry/nextjs vitest --no-audit"
    
    try:
        # shell=True necessário no Windows
        subprocess.run(cmd, cwd=frontend_dir, shell=True, check=True)
        print("✅ Dependências instaladas com sucesso.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha ao instalar dependências: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(fix())
