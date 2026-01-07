# 🔌 Guia do Hub de Integrações (Developer Guide)

## 1. Webhooks de Saída (Outgoing Webhooks)
O MesaFlow notifica sistemas externos sobre eventos em tempo real.

### Segurança (Assinatura HMAC)
Todas as requisições contêm o cabeçalho `X-MesaFlow-Signature`.
**Como validar (Exemplo Python):**
```python
import hmac, hashlib
signature = hmac.new(secret.encode(), payload_body.encode(), hashlib.sha256).hexdigest()
assert signature == request.headers["X-MesaFlow-Signature"]
```

### Eventos Suportados
- `order.created`: Disparado assim que o pedido entra no banco.
- `order.updated`: Disparado em mudanças de status (ex: `preparing` -> `ready`).
- `payment.updated`: Disparado na confirmação do pagamento.

## 2. Integração iFood
O MesaFlow atua como um agregador.
- **Polling:** O sistema consulta o iFood a cada 30s.
- **Acknowledge:** O MesaFlow confirma o recebimento para o iFood apenas após o pedido ser persistido com sucesso no nosso banco.
- **Mapeamento:** Certifique-se de que o `external_id` do produto no MesaFlow seja idêntico ao `merchant_id` ou `SKU` no portal do iFood.

---
# 🔌 Hub de Integrações: Especificação para Desenvolvedores

## 1. Webhooks de Saída
O MesaFlow envia um POST JSON para sua URL sempre que um evento ocorre.

### Exemplo de Payload (`order.created`)
```json
{
  "event": "order.created",
  "timestamp": "2026-01-05T20:00:00Z",
  "data": {
    "id": "uuid-do-pedido",
    "total_amount": 150.50,
    "origin": "mesaflow",
    "items": [
      {"name": "Pizza", "qty": 1, "price": 50.00}
    ]
  }
}
```

### Validação de Segurança
O header `X-MesaFlow-Signature` contém o hash do corpo da requisição.
```python
# Exemplo de validação em Python/FastAPI
import hmac, hashlib
def verify(body: bytes, signature: str, secret: str):
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## 2. Mapeamento iFood (SKU Sync)
Para que a integração funcione, o campo `external_id` no MesaFlow deve bater com o `Merchant SKU` no iFood.
- Se o iFood enviar um item não mapeado, o sistema criará o pedido com um "Item Genérico" e alertará o gestor no KDS.

---
