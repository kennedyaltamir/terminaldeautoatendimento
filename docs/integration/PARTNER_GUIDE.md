🤝 Guia de Integração para Parceiros (ERPs)

Este guia é destinado a desenvolvedores de sistemas de gestão (ERPs, PDVs Fiscais) que desejam integrar com o MesaFlow.

Base URL: https://api.mesaflow.com.br/api

1. Autenticação

Utilizamos API Keys para parceiros.

O cliente deve gerar uma chave em: Painel Admin > Configurações > Integrações.

Envie a chave no Header: X-API-Key: sk_live_...

2. Webhooks (Recebendo Dados)

A maneira mais eficiente de sincronizar pedidos é ouvindo nossos webhooks.

Eventos Suportados:

order.created: Novo pedido realizado.

order.status_changed: Pedido pronto/entregue.

order.payment_updated: Pagamento confirmado.

Payload Exemplo (order.created):

code
JSON
download
content_copy
expand_less
{
  "event": "order.created",
  "timestamp": "2026-01-05T10:00:00Z",
  "data": {
    "id": "uuid-do-pedido",
    "total": 150.00,
    "items": [
      { "sku": "XBACON", "qty": 2, "price": 25.00 }
    ],
    "customer": { "name": "João", "phone": "11999999999" }
  }
}
3. Endpoints Principais
GET /admin/{slug}/orders

Lista pedidos ativos. Útil para sincronização inicial ou fallback de webhook.

Filtros: ?status=pending,ready & ?date=2026-01-05

POST /admin/menu/products

Sincronização de catálogo. Permite que o ERP crie/atualize produtos no MesaFlow.

Campos Chave: short_code (Código PDV), price, stock_quantity.

PATCH /admin/inventory/ingredients/{id}

Atualização de estoque. O ERP pode enviar o saldo atual de ingredientes para o MesaFlow bloquear vendas.

4. Limites (Rate Limits)

Webhooks: Retry automático 3x (exponencial).

API: 60 requisições/minuto por Token.
