# 🚀 Especificação Técnica: TASK-MAINT-05
> **Título:** Configuração e Ativação do Redis (Cache & Real-time)
> **Status:** APROVADO
> **Objetivo:** Garantir que o motor de cache e WebSockets (Redis) esteja operacional no ambiente Windows.

## 1. Contexto
O MesaFlow utiliza Redis para:
- **WebSockets:** Sincronização entre múltiplos workers (KDS/Garçom).
- **Cache L2:** Performance do cardápio público.
- **Blacklist:** Revogação imediata de tokens JWT.

## 2. Estratégia de Implementação
No Windows, a forma mais estável de rodar o Redis é via **Docker**.
- Utilizar a imagem `redis:alpine`.
- Mapear a porta `6379:6379`.
- Persistência via volume `redis_data`.

## 3. Requisitos
- Docker Desktop instalado e rodando.
- Variável `REDIS_URL` no `.env` apontando para `redis://localhost:6379/0`.
