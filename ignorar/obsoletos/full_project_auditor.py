# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 19:00:00
import os
import sys
import socket
from pathlib import Path

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_auditor():
    print("🛡️  MesaFlow Full Project Auditor v1.1")
    print("======================================")
    
    errors = 0

    # 1. Auditoria de Sintaxe Frontend
    print("\n[1/4] Auditando Sintaxe TypeScript...")
    api_ts = Path("frontend/src/lib/api.ts")
    if api_ts.exists():
        content = api_ts.read_text(encoding="utf-8")
        
        # Verificação exata da linha de headers
        if "...options.headers," in content:
            print("✅ api.ts: Spread operator correto.")
        else:
            print("❌ ERRO: api.ts possui sintaxe de headers inválida.")
            errors += 1
            
        if "# DOMAIN" in content:
            print("❌ ERRO: api.ts possui comentários de metadados inválidos (#).")
            errors += 1
    else:
        print("⚠️  AVISO: api.ts não encontrado.")

    # 2. Auditoria de Infraestrutura Local
    print("\n[2/4] Auditando Serviços Locais...")
    if check_port(5432):
        print("✅ PostgreSQL: Online")
    else:
        print("❌ PostgreSQL: Offline (Porta 5432)")
        errors += 1

    if check_port(6379):
        print("✅ Redis: Online")
    else:
        print("⚠️  Redis: Offline (Porta 6379)")

    # 3. Auditoria de Ambiente (.env)
    print("\n[3/4] Auditando Configurações (.env)...")
    env_path = Path(".env")
    if env_path.exists():
        content = env_path.read_text(encoding="utf-8")
        if "psql " in content:
            print("❌ ERRO: Prefixo 'psql' detectado na DATABASE_URL")
            errors += 1
    else:
        print("❌ ERRO: Arquivo .env ausente.")
        errors += 1

    # 4. Auditoria de Dependências
    print("\n[4/4] Auditando node_modules...")
    if Path("frontend/node_modules").exists():
        print("✅ node_modules: OK")
    else:
        print("❌ node_modules: Ausente. Rode 'npm install' na pasta frontend.")
        errors += 1

    print("\n" + "="*38)
    if errors == 0:
        print("✨ PROJETO ÍNTEGRO: Pronto para rodar.")
    else:
        print(f"🚨 DETECTADOS {errors} ERROS CRÍTICOS.")
    print("="*38)

if __name__ == "__main__":
    run_auditor()