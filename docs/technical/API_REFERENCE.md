# 🔌 API Reference - MesaFlow v2.3.0

Esta documentação detalha os contratos de integração com a API do MesaFlow.

## 🏢 1. Contexto Público (Cliente)
Endpoints que não requerem token administrativo.

### `GET /api/{slug}/menu`
Retorna a estrutura completa da loja.
- **Cache:** 5 minutos (Redis Layer 2).
- **Filtro:** Apenas categorias e produtos ativos no horário atual.

### `POST /api/{slug}/orders`
Cria um pedido na comanda ou delivery.
- **Rate Limit:** 10 requisições/min por IP.

---

## 🔐 2. Autenticação e Segurança
Acesso protegido para Staff e Donos.

### `POST /api/auth/google`
Realiza login ou cadastro automático via Google.
- **Payload:** `{ "credential": "ID_TOKEN_DO_GOOGLE" }`

### `GET /api/admin/audit`
Consulta logs de auditoria (Ações críticas).
- **Otimização:** Filtro por `company_id` e `created_at` indexado.

---

## 📊 3. Operação e Dados
Gestão de alta performance.

### `GET /api/admin/metrics`
Dados agregados para o dashboard.
- **Performance:** Queries SQL otimizadas com índices compostos.

### `PATCH /api/admin/orders/{id}`
Muda o status do pedido (KDS).
- **Triggers:** Dispara notificações via WebSocket e WhatsApp.

---

## 🛠️ Erros Comuns
| Código | Descrição |
| :--- | :--- |
| `401` | Token ausente ou expirado. |
| `403` | Empresa A tentando acessar recurso da Empresa B (Anti-IDOR). |
| `422` | Payload malformado ou campos faltando. |
| `429` | Limite de requisições excedido. |
# 🔌 API Reference - MesaFlow v3.0.0

## 1. Autenticação
Acesse `/api/auth/token` para obter seu Bearer JWT.

## 2. Webhooks de Saída (Outgoing Webhooks)
O MesaFlow notifica seu sistema sobre eventos em tempo real.

### Eventos Disponíveis:
- `order.created`: Novo pedido (Mesa, Delivery ou iFood).
- `order.updated`: Mudança de status na cozinha.
- `payment.updated`: Confirmação de pagamento.

### Segurança:
Valide o header `X-MesaFlow-Signature` usando seu **Signing Secret**. O hash é gerado via HMAC-SHA256 sobre o corpo bruto (raw body) da requisição.

## 3. Integração iFood
Para que os pedidos do iFood sejam mapeados corretamente:
1. Cadastre o `ifood_merchant_id` nas configurações da empresa.
2. No cadastro de produtos, preencha o campo `external_id` com o SKU correspondente no portal do iFood.

## 4. Documentação Interativa
- **Swagger UI:** `/docs` (Recomendado para testes rápidos).
- **ReDoc:** `/redoc` (Recomendado para leitura técnica).

---
