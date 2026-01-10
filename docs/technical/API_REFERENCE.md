# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 10:45:00
# 🔌 API Reference - MesaFlow v3.1.0

Esta documentação detalha os contratos de integração com a API do MesaFlow, consolidando endpoints públicos, administrativos e de integração.

> **⚠️ MUDANÇA CRÍTICA (v3.1): PADRÃO MONETÁRIO**
> Todos os valores monetários agora trafegam como **Inteiros (Centavos)** para evitar erros de ponto flutuante.
> - **Antes:** `10.50` (Float/Decimal)
> - **Agora:** `1050` (Integer)
>
> *Exemplo: R$ 100,00 deve ser enviado como `10000`.*

---

## 🏢 1. Contexto Público (Cliente Final)
Endpoints que não requerem token administrativo.

### `GET /api/{slug}/menu`
Retorna a estrutura completa da loja (Categorias, Produtos, Opções).
- **Cache:** 5 minutos (Redis Layer 2).
- **Response:** Preços em centavos (`price: 2590` = R$ 25,90).
- **Filtro:** Retorna apenas itens ativos e dentro do horário de funcionamento.

### `POST /api/{slug}/orders`
Cria um pedido na comanda ou delivery.
- **Payload:** `total_amount` e `unit_price` devem ser enviados em centavos.
- **Rate Limit:** 10 requisições/min por IP.

---

## 🔐 2. Autenticação e Segurança
Acesso protegido para Staff e Donos.

### `POST /api/auth/token`
Login tradicional (OAuth2 Password Flow).
- **Response:** JWT contendo `access_token`, `refresh_token` e `company_id` (essencial para o contexto RLS).

### `POST /api/auth/google`
Realiza login ou cadastro automático via Google.
- **Payload:** `{ "credential": "ID_TOKEN_DO_GOOGLE" }`

---

## 📊 3. Operação e Gestão (Admin)
Endpoints protegidos (Requer Header `Authorization: Bearer <TOKEN>`).

### `GET /api/admin/metrics`
Dados agregados para o dashboard (Faturamento, Ticket Médio, Heatmap).
- **Performance:** Queries SQL otimizadas com índices compostos.

### `GET /api/admin/audit`
Consulta logs de auditoria (Ações críticas como deleção, login, alteração de preço).
- **Segurança:** Filtro obrigatório por `company_id` via RLS.

### `PATCH /api/admin/orders/{id}`
Muda o status do pedido (KDS).
- **Triggers:** Dispara notificações via WebSocket (KDS/App) e WhatsApp (Cliente).

---

## 📡 4. Webhooks & Integrações

### 4.1 Inbound Webhooks (Recebimento)
Endpoints para receber eventos de plataformas externas.

- **`POST /api/webhooks/ifood`**
    - Recebe atualizações de pedidos (`PLACED`, `CONFIRMED`, `CANCELLED`).
    - **Segurança:** Requer header `x-ifood-signature` (HMAC-SHA256).

- **`POST /api/webhooks/stripe`**
    - Atualizações de assinatura SaaS (Renovação, Cancelamento).
    - **Segurança:** Requer header `stripe-signature`.

### 4.2 Outgoing Webhooks (Envio)
O MesaFlow notifica seu sistema externo sobre eventos em tempo real.

- **Eventos Disponíveis:**
    - `order.created`: Novo pedido (Mesa, Delivery ou iFood).
    - `order.updated`: Mudança de status na cozinha.
    - `payment.updated`: Confirmação de pagamento.
- **Segurança:** Valide o header `X-MesaFlow-Signature` usando seu **Signing Secret**.

### 4.3 Mapeamento iFood
Para que a integração funcione corretamente:
1. Cadastre o `ifood_merchant_id` nas configurações da empresa.
2. No cadastro de produtos, preencha o campo `external_id` com o SKU correspondente no portal do iFood.

---

## 📚 5. Documentação Interativa
Para testar os endpoints diretamente:

- **Swagger UI:** `/docs` (Ambiente de teste e exploração).
- **ReDoc:** `/redoc` (Documentação técnica detalhada).

---

## 🛠️ 6. Tabela de Erros Comuns

| Código | Descrição |
| :--- | :--- |
| `401` | **Unauthorized:** Token ausente, expirado ou inválido. |
| `403` | **Forbidden:** Assinatura de Webhook inválida ou Acesso negado pelo RLS (Tentativa de acessar dados de outro tenant). |
| `404` | **Not Found:** Recurso não encontrado (ou oculto pelo RLS). |
| `422` | **Unprocessable Entity:** Payload malformado (ex: enviar float em campo de centavos). |
| `429` | **Too Many Requests:** Limite de requisições excedido. |
