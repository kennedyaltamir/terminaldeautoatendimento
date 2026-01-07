🔐 Segurança de Webhooks

Para garantir que os eventos recebidos no seu servidor realmente vieram do MesaFlow, você deve validar a assinatura HMAC.

1. O Cabeçalho

Cada requisição POST enviada pelo MesaFlow contém o header:
X-MesaFlow-Signature: Hash SHA-256 do payload.

2. Como Validar (Exemplo Python)
code
Python
download
content_copy
expand_less
import hmac
import hashlib
import json

def verify_signature(request_body: bytes, signature: str, secret: str) -> bool:
    """
    request_body: O corpo bruto (raw bytes) da requisição.
    signature: O valor do header X-MesaFlow-Signature.
    secret: O segredo do webhook configurado no painel do MesaFlow.
    """
    expected_signature = hmac.new(
        key=secret.encode(),
        msg=request_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)
3. Boas Práticas

Idempotência: O mesmo evento pode ser enviado mais de uma vez (em caso de falha de rede). Use o campo id do evento para evitar processamento duplicado.

Timeout: Responda com 200 OK rapidamente (em menos de 3 segundos). Processe a lógica pesada em background.

HTTPS: Seu endpoint deve obrigatoriamente usar SSL.
