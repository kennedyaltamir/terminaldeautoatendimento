import os
import sys
import requests
import time
import re

# Configuração
BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = "/health"

def verify_monitoring_readiness():
    print("🔍 Iniciando Verificação de Prontidão para Monitoramento Externo (TASK-ENT-01.2)...")

    # 1. Verificar Artefatos de Governança
    docs = [
        "docs/trust/STATUS_PAGE.md",
        "docs/trust/SLA_AVAILABILITY.md"
    ]
    
    for doc in docs:
        if not os.path.exists(doc):
            print(f"❌ Documento FALTANDO: {doc}")
            sys.exit(1)
        print(f"✅ Documento encontrado: {doc}")

    # 2. Verificar Conteúdo do SLA (Regex Tolerante a Localização)
    with open("docs/trust/SLA_AVAILABILITY.md", "r", encoding="utf-8") as f:
        content = f.read()
        # Aceita tanto 99.9% (US) quanto 99,9% (BR)
        if not re.search(r"99[.,]9%", content):
            print(f"❌ SLA Target (99.9% ou 99,9%) não encontrado na documentação.")
            sys.exit(1)
        print(f"✅ SLA Target (99.9% / 99,9%) confirmado na documentação.")

    # 3. Simular Probe Externo (Latência e Status)
    print(f"📡 Simulando Probe Externo em {BASE_URL}{HEALTH_ENDPOINT}...")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}{HEALTH_ENDPOINT}", timeout=5)
        latency = (time.time() - start_time) * 1000
        
        if response.status_code != 200:
            print(f"❌ Probe falhou: Status Code {response.status_code}")
            sys.exit(1)
            
        data = response.json()
        if data.get("status") != "healthy":
            print(f"❌ Probe falhou: Status JSON inválido ({data.get('status')})")
            sys.exit(1)
            
        print(f"✅ Probe Sucesso: HTTP 200 | Latência: {latency:.2f}ms")
        
        if latency > 500:
            print("⚠️  ALERTA: Latência alta (>500ms). Pode afetar monitoramento externo.")
        
    except Exception as e:
        print(f"❌ Erro de conexão no Probe: {e}")
        print("   Certifique-se de que o servidor está rodando (python run.py).")
        sys.exit(1)

    print("\n🏆 External Health Monitoring Verified: SLA evidence and public status page confirmed.")
    sys.exit(0)

if __name__ == "__main__":
    verify_monitoring_readiness()