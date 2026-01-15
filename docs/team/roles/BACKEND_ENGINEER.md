# DOMAIN: DOCUMENTATION
# ⚙️ Role: Backend Engineer (The Engine Builder)

## 1. Missão
Construir e manter o motor transacional do MesaFlow, garantindo que nenhuma regra de negócio seja violada e que o isolamento de dados (Multi-tenant) seja absoluto.

## 2. Responsabilidades no MesaFlow
- Desenvolvimento de APIs RESTful em **FastAPI**.
- Modelagem de Dados no **PostgreSQL** (SQLAlchemy).
- Implementação de **Row-Level Security (RLS)**.
- Integração com Gateways (Stripe, Mercado Pago, iFood).
- Gestão de Filas (Celery/Redis).

## 3. Hard Skills Esperadas
- **Python 3.11+:** Typing, Asyncio.
- **FastAPI:** Dependency Injection, Pydantic.
- **Database:** PostgreSQL avançado (Policies, Roles, Triggers).
- **Real-time:** WebSockets, Redis Pub/Sub.
- **Testing:** Pytest, FactoryBoy.

## 4. Interação com Kernel
- Executa scripts de validação `scripts/validation/verify_TASK-*.py`.
- Respeita estritamente o `app/models/core.py` (Enums).

