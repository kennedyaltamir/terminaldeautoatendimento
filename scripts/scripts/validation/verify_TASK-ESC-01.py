import sys
import os
import hmac
import hashlib
import json
from fastapi.testclient import TestClient

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.main import app

client = TestClient(app)

def verify():
    print("🔍 Verificando TASK-ESC-01: iFood Webhooks...")

    # 1. Configuração de Teste
    secret = "default_secret_change_me" # Valor padrão do código
    os.environ["IFOOD_WEBHOOK_SECRET"] = secret
    
    payload = {
        "id": "evt-123",
        "code": "PLACED",
        "orderId": "ord-ifood-test",
        "merchantId": "merch-123"
    }
    body = json.dumps(payload).encode()
    
    # 2. Teste de Assinatura Inválida
    print("🧪 Teste 1: Assinatura Inválida...")
    res_invalid = client.post(
        "/api/webhooks/ifood",
        content=body,
        headers={"x-ifood-signature": "invalid_sig"}
    )
    if res_invalid.status_code == 403:
        print("✅ Bloqueio de segurança OK.")
    else:
        print(f"❌ Falha: Aceitou assinatura inválida (Status {res_invalid.status_code})")
        sys.exit(1)

    # 3. Teste de Assinatura Válida
    print("🧪 Teste 2: Assinatura Válida...")
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    
    res_valid = client.post(
        "/api/webhooks/ifood",
        content=body,
        headers={"x-ifood-signature": signature}
    )
    
    if res_valid.status_code == 200:
        print("✅ Webhook aceito com sucesso.")
    else:
        print(f"❌ Falha: Rejeitou assinatura válida (Status {res_valid.status_code})")
        print(res_valid.json())
        sys.exit(1)

    print("\n🏆 TASK-ESC-01: VALIDAÇÃO CONCLUÍDA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
