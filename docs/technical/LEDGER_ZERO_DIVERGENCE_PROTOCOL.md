# 💰 Protocolo de Divergência Zero: Ledger L7 & ERP v2.0
**Versão:** 10.0.2-AUTO | **Domínio:** FINTECH | **Status:** ENFORCED

## 1. Mapeamento de Divergências Residuais
| Cenário de Divergência | Causa Raiz | Threshold Proativo (L10.2) |
| :--- | :--- | :--- |
| **Chargeback** | Disputa do cliente no cartão | `webhook: chargeback.created` |
| **Refund Parcial** | Estorno de item individual | Divergência entre `order.total` e `transaction.amount` |
| **Taxa do Gateway** | Mudança de taxa não comunicada | `transaction.net_amount` != `order.total - expected_fee` |

## 2. Validação Contínua Zero-Latency via Stream Processing
- **Mecanismo:** O webhook do gateway (Mercado Pago/Stripe) não escreve mais diretamente no DB. Ele publica o evento em um **tópico Kafka/Redis Stream**.
- **Processador de Stream:** Um worker Celery dedicado consome o evento, compara com o **Shadow Ledger** em Redis em tempo real, e só então commita a transação no PostgreSQL.
- **Benefício:** A validação ocorre em milissegundos, antes que o dado se torne "verdade" no banco de dados.

## 3. Triggers de Investigação Automática (Pagamentos `pending`)
- **Regra:** Se `payment_transactions.status` permanecer `pending` por > 30 minutos, o sistema dispara a task `investigate_pending_payment`.
- **Ação Preventiva:** A task consulta a API do gateway. Se o pagamento não existir, o registro é marcado como `expired` e um evento `payment.failed` é emitido. Isso libera o estoque e notifica o cliente.

