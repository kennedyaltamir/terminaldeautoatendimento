import requests
import sys
import csv
import io

# Configuração
BASE_URL = "http://localhost:8000/api"

def verify_audit_export():
    print("🔍 Iniciando Verificação de Exportação de Auditoria (TASK-ENT-08)...")

    # 1. Obter Token de Admin (Owner)
    # Assume que o usuário admin padrão existe (seed)
    try:
        auth_res = requests.post(f"{BASE_URL}/auth/token", data={"username": "admin@mesaflow.com", "password": "123456"})
        if auth_res.status_code != 200:
            print("❌ Falha na autenticação para teste.")
            sys.exit(1)
        token = auth_res.json()["access_token"]
    except Exception as e:
        print(f"❌ Erro de conexão ao autenticar: {e}")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Requisitar Exportação
    print("📥 Solicitando exportação CSV...")
    try:
        res = requests.get(f"{BASE_URL}/admin/audit/export", headers=headers, stream=True)
        
        if res.status_code != 200:
            print(f"❌ Erro na exportação: Status {res.status_code}")
            print(res.text)
            sys.exit(1)
        
        # Verificar Content-Type
        ctype = res.headers.get("Content-Type", "")
        if "text/csv" not in ctype:
            print(f"❌ Content-Type incorreto: {ctype}")
            sys.exit(1)

        # 3. Validar Estrutura do CSV
        content = res.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        header = next(reader, None)

        if not header:
            print("❌ CSV vazio ou inválido.")
            sys.exit(1)

        expected_header = ["Timestamp", "Actor", "Role", "Action", "Resource", "Resource ID", "IP Address", "Details"]
        
        if header != expected_header:
            print(f"❌ Cabeçalho CSV incorreto.\nEsperado: {expected_header}\nRecebido: {header}")
            sys.exit(1)

        print(f"✅ CSV gerado com sucesso. Tamanho: {len(content)} bytes.")
        
    except Exception as e:
        print(f"❌ Erro durante a verificação: {e}")
        sys.exit(1)

    print("\n🏆 Audit Export Verified: CSV generated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    verify_audit_export()
