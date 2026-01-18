# 🔌 Matriz de SLAs e Resiliência Externa
**Versão:** 5.0.2-SEQ | **Domínio:** INFRASTRUCTURE

| Serviço | SLA Alvo | Timeout | Estratégia de Fallback |
| :--- | :---: | :---: | :--- |
| **Mercado Pago** | 99.9% | 10s | Switch para Pix Estático (Manual) |
| **Stripe** | 99.99% | 15s | Cache de Assinatura (Grace Period 72h) |
| **FocusNFe** | 99.5% | 30s | Fila de Contingência Offline (Dexie.js) |
| **Evolution API** | 98.0% | 5s | Silent Fail + Log de Auditoria |

## 1. Tolerância a Falhas Offline-First
- **Inconsistência de Estoque:** O Mobile POS permite venda "no escuro" se offline, mas marca o pedido com a flag `inventory_risk: true` para conferência manual pós-sync.
- **Pagamento Offline:** Proibido para cartões/pix dinâmico. Permitido apenas para "Dinheiro" ou "Pix Estático".

