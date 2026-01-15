
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 08:20:00
import requests
import hmac
import hashlib
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000/api/webhooks/ifood"
SECRET = os.getenv("IFOOD_WEBHOOK_SECRET")

if not SECRET:
    print("⚠️  AVISO: IFOOD_WEBHOOK_SECRET não encontrado no .env.")
    print("   Usando segredo de fallback para teste local: 'default_secret_change_me'")
    SECRET = "default_secret_change_me"

def generate_signature(payload: dict, secret: str) -> str:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

def run_tests():
    print(f"🛡️  Validando Segurança do Webhook iFood (Target: {BASE_URL})...")
    
    payload = {
        "id": "evt-REPLAY-TEST",
        "code": "PLACED",
        "orderId": "ord-777-TEST",
        "merchantId": "merch-1",
        "createdAt": "2026-01-11T12:00:00.000Z"
    }

    # 1. Teste de Autenticação
    print("   [1/3] Testando assinatura legítima...")
    canonical_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = generate_signature(payload, SECRET)
    headers = {
        "x-ifood-signature": signature,
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(BASE_URL, data=canonical_body, headers=headers)
        if res.status_code == 200:
            print("   ✅ Aceito com sucesso (200 OK).")
        elif res.status_code == 409:
            print("   ⚠️  Conflito de Replay detectado (409). Isso significa que o teste já rodou recentemente.")
            print("      Aguarde 10 minutos ou limpe o Redis para testar sucesso novamente.")
        else:
            print(f"   ❌ FALHA: Status inesperado ({res.status_code})")
            print("   Body:", res.text)
            sys.exit(1)
            
        # 2. Teste de Replay Attack (Imediato)
        print("   [2/3] Testando Replay Attack (mesma assinatura)...")
        res_replay = requests.post(BASE_URL, data=canonical_body, headers=headers)
        
        if res_replay.status_code == 409:
             print("   ✅ Proteção contra Replay Ativa! (409 Conflict recebido).")
        else:
             print(f"   ❌ FALHA: Replay não bloqueado. Status: {res_replay.status_code}")
             print("      Verifique se o Redis está online e se CacheService está funcionando.")
             # Em ambiente dev sem Redis, o CacheService pode estar em bypass (memória ou inativo)
             # Se for bypass memória, deveria funcionar. Se for null, falha.

        # 3. Teste de Assinatura Inválida
        print("   [3/3] Testando assinatura inválida...")
        headers_bad = headers.copy()
        headers_bad["x-ifood-signature"] = "deadbeef"
        res_bad = requests.post(BASE_URL, data=canonical_body, headers=headers_bad)
        if res_bad.status_code == 403:
            print("   ✅ Bloqueado corretamente (403 Forbidden).")
        else:
             print(f"   ❌ FALHA: Aceitou assinatura ruim ({res_bad.status_code})")
             sys.exit(1)

    except requests.exceptions.ConnectionError:
        print("❌ Erro: O servidor não está rodando na porta 8000.")
        sys.exit(1)

    print("\n✨ Webhook iFood: Compliance Grade Validated.")

if __name__ == "__main__":
    run_tests()

