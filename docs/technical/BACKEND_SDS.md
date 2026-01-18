# ⚙️ Software Design Specification: Backend
**Domínio:** BACKEND | **Versão:** 5.0

## 1. Camadas de Responsabilidade
- **Routers (`app/routers/`):** Entrypoints REST e WebSocket. Validação de schemas Pydantic e injeção de contexto de Tenant.
- **Services (`app/services/`):** Lógica de negócio pura. Orquestração de transações e integração com gateways.
- **Models (`app/models/`):** Definição de tabelas SQLAlchemy com suporte nativo a RLS.
- **Core (`app/core/`):** Segurança (JWT), Circuit Breaker, Logger JSON e limites de IA.

## 2. Fluxos Críticos
### 2.1. Criação de Pedido e RLS
1. Request chega com `company_slug`.
2. Middleware resolve `company_id`.
3. `get_db` executa `SET row_security = on`.
4. `set_tenant` injeta `app.current_company_id` na sessão.
5. Banco bloqueia qualquer dado que não pertença ao Tenant.

### 2.2. Ledger Financeiro (L7)
Toda transação financeira gera uma entrada na tabela `financial_ledger`:
- `sequence_id`: Gerado via IDENTITY do Postgres.
- `integrity_hash`: `SHA256(prev_hash | company_id | amount | type | balance | ref)`.
- **Imutabilidade:** Proibido UPDATE/DELETE via política de banco.

## 3. Tarefas Assíncronas (Celery)
- **Webhook Dispatcher:** Envio de eventos para integradores externos com retry exponencial.
- **Fiscal Emission:** Processamento de notas fiscais (NFC-e) em background para não travar a API.
- **Stock Alerts:** Notificações de estoque baixo via WhatsApp.

## 4. Mapa de Rotas (Principais)
| Método | Rota | Serviço | Função |
| :--- | :--- | :--- | :--- |
| POST | `/api/auth/token` | `security.py` | Geração de JWT |
| GET | `/api/{slug}/menu` | `cache.py` | Cardápio (Cache 5min) |
| PATCH | `/api/admin/delivery/orders/{id}/dispatch` | `order_service.py` | Início de rota (Idempotente) |
| POST | `/api/admin/delivery/orders/{id}/location` | `driver_service.py` | Injeção de GPS |

