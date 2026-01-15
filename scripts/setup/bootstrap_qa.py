# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 18:20:00
import subprocess
import sys
import os
from pathlib import Path

# ==============================================================================
# 🥾 QA BOOTSTRAPPER v1.1 (Fixed Pip & Node Paths)
# ==============================================================================

def run_cmd(cmd, cwd=None):
    print(f"🛠️  Executando: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError:
        return False

def bootstrap():
    print("====================================================")
    print("📦 MESAFLOW QA DEPENDENCY BOOTSTRAP")
    print("====================================================")

    # 1. Python Deps
    print("\n[1/3] Verificando dependências Python...")
    # FIX: Removido --no-audit que não existe no pip
    run_cmd(f"{sys.executable} -m pip install pytest pytest-asyncio httpx")

    # 2. Frontend Deps (Node.js)
    print("\n[2/3] Verificando dependências de Frontend...")
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Erro: Pasta 'frontend' não encontrada.")
        return

    # Instala o runner de teste como devDependency
    run_cmd("npm install -D @playwright/test --no-audit", cwd="frontend")

    # 3. Playwright Browsers
    print("\n[3/3] Instalando binários dos navegadores (Chromium)...")
    run_cmd("npx playwright install chromium", cwd="frontend")

    print("\n✅ QA BOOTSTRAP CONCLUÍDO.")
if __name__ == "__main__":
    bootstrap()

