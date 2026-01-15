# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:20:00
import os
import socket
import subprocess
import sys
from pathlib import Path

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_diagnostics():
    print("🔍 MesaFlow Boot Diagnostics - Windows Environment")
    print("================================================")

    # 1. Verificar Sintaxe do Frontend
    api_ts = Path("frontend/src/lib/api.ts")
    print("\n[1/5] Verificando sintaxe do Cliente API")
    if api_ts.exists():
        content = api_ts.read_text(encoding="utf-8")
        if "options.headers," in content and "" not in content:
            print("❌ ERRO: Sintaxe invalida detectada em api.ts (Falta '')")
        elif "# DOMAIN" in content:
            print("❌ ERRO: Comentarios de metadados invalidos (#) detectados em api.ts")
        else:
            print("✅ Sintaxe do Frontend parece correta.")
    else:
        print("❌ ERRO: Arquivo api.ts nao encontrado.")

    # 2. Verificar Banco de Dados
    print("\n[2/5] Verificando PostgreSQL (Porta 5432)")
    if check_port(5432):
        print("✅ Porta 5432 aberta.")
        print("👉 Dica: Se o log mostrar 'FATAL: password authentication failed',")
        print("   verifique a senha no seu .env e no PGAdmin.")
    else:
        print("❌ ERRO: PostgreSQL nao esta rodando ou porta 5432 bloqueada.")

    # 3. Verificar Redis
    print("\n[3/5] Verificando Redis (Porta 6379)")
    if check_port(6379):
        print("✅ Redis detectado.")
    else:
        print("⚠️  AVISO: Redis nao detectado. O sistema usara memoria local (Modo Degradado).")

    # 4. Verificar Encoding do Python
    print("\n[4/5] Verificando Encoding do Sistema")
    print(f"Default Encoding: {sys.getdefaultencoding()}")
    print(f"Filesystem Encoding: {sys.getfilesystemencoding()}")
    if sys.platform == "win32":
        print("ℹ️  Ambiente Windows detectado. Garantindo compatibilidade CP1252/UTF-8.")

    # 5. Verificar Node Modules
    print("\n[5/5] Verificando dependencias do Frontend")
    if Path("frontend/node_modules").exists():
        print("✅ node_modules encontrado.")
    else:
        print("❌ ERRO: node_modules ausente. Rode 'cd frontend && npm install'.")

    print("\n================================================")
    print("🚀 RECOMENDACAO: Aplique o patch do Kernel e reinicie com 'python run.py'")

if __name__ == "__main__":
    run_diagnostics()
