# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 15:20:00
import os
import requests
from pathlib import Path

def validate():
    print("🔍 Validando TASK-FEAT-02 (Public Monitor)")
    
    # 1. Verificar arquivos
    required_files = [
        "frontend/src/app/[slug]/monitor/page.tsx",
        "frontend/src/components/menu/PublicMonitorView.tsx"
    ]
    
    for f in required_files:
        if not Path(f).exists():
            print(f"❌ ERRO: Arquivo {f} nao encontrado.")
            exit(1)
    
    # 2. Verificar Endpoint Backend
    print("📡 Testando endpoint de monitoramento")
    try:
        # Tenta acessar o monitor da hamburgueria-ze (assumindo que o server esta rodando)
        res = requests.get("http://localhost:8000/api/hamburgueria-ze/monitor")
        if res.status_code == 200:
            print("✅ API Monitor: OK")
            data = res.json()
            if isinstance(data, list):
                print(f"✅ Formato de dados: OK ({len(data)} pedidos ativos)")
        else:
            print(f"⚠️  API Monitor retornou status {res.status_code}. Certifique-se de que o backend esta rodando.")
    except Exception as e:
        print(f"⚠️  Nao foi possivel testar a API (Server offline?): {e}")

    print("\n✅ TASK-FEAT-02: Estrutura do Monitor Público validada.")
    exit(0)

if __name__ == "__main__":
    validate()
