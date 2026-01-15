# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 15:18:00
import os
import socket
import sys
from pathlib import Path

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def verify_file_content(file_path, search_str):
    if not os.path.exists(file_path):
        return False, "Arquivo não encontrado"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return search_str in content, "Encontrado" if search_str in content else "Não encontrado"
    except Exception as e:
        return False, str(e)

def run_audit():
    print("🔍 MesaFlow Deep System Audit v1.0")
    print("==================================")

    # 1. Syntax Check (Frontend)
    api_ts = "frontend/src/lib/api.ts"
    print(f"\n[1/5] Verificando sintaxe em {api_ts}")
    ok, msg = verify_file_content(api_ts, "options.headers,")
    if ok:
        print("✅ Sintaxe do spread operator: OK")
    else:
        print(f"❌ ERRO: Sintaxe incorreta detectada. Esperado 'options.headers,'.")

    # 2. Redis Check
    print("\n[2/5] Verificando Redis (Porta 6379)")
    if check_port(6379):
        print("✅ Redis está rodando.")
    else:
        print("❌ ERRO: Redis não detectado. Verifique se o serviço está ativo.")

    # 3. Database Check
    print("\n[3/5] Verificando PostgreSQL (Porta 5432)")
    if check_port(5432):
        print("✅ PostgreSQL está rodando.")
    else:
        print("❌ ERRO: PostgreSQL não detectado.")

    # 4. .env Check
    print("\n[4/5] Validando arquivo .env")
    if os.path.exists(".env"):
        print("✅ Arquivo .env presente.")
        # Verifica se há prefixos de CLI na URL
        ok, msg = verify_file_content(".env", "psql ")
        if ok:
            print("❌ ERRO: Variável DATABASE_URL contém prefixo 'psql '. Remova-o.")
    else:
        print("❌ ERRO: Arquivo .env ausente.")

    # 5. Encoding Check
    print("\n[5/5] Verificando codificação do sistema")
    print(f"Python Default Encoding: {sys.getdefaultencoding()}")
    if sys.platform == "win32":
        print("ℹ️  Ambiente Windows detectado. Caracteres especiais em logs podem exigir tratamento.")

    print("\n==================================")
    print("🚀 RECOMENDAÇÃO: Aplique o patch do Kernel e limpe o cache do Next.js.")

if __name__ == "__main__":
    run_audit()
