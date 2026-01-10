# 📈 Planejamento de Capacidade e Performance

**Versão:** 1.0
**Data:** Janeiro de 2026
**Escopo:** Infraestrutura PaaS (Render + Neon)

## 1. Baseline de Performance (SLA Interno)

| Métrica | Alvo (Target) | Limite (Threshold) | Ação no Limite |
| :--- | :---: | :---: | :--- |
| **Latência API (p95)** | < 200ms | > 500ms | Escalar Workers (Horizontal) |
| **Latência DB (Query)** | < 50ms | > 100ms | Otimizar Índices / Cache L2 |
| **Taxa de Erro** | < 0.1% | > 1% | Rollback / Circuit Breaker |
| **Uptime** | 99.9% | < 99.5% | Acionar DR (Disaster Recovery) |

## 2. Capacidade Estimada (Plano Starter)

Com a configuração atual (`WEB_CONCURRENCY=4`, Neon Pooled), estimamos:

- **RPS Sustentável:** ~100 req/s (Backend)
- **Usuários Simultâneos:** ~500 (Navegando/Pedindo)
- **Pedidos por Minuto:** ~60 (1 por segundo)

## 3. Estratégia de Escala

### Nível 1: Aplicação (Stateless)
O backend FastAPI é stateless. Para escalar:
1. Aumentar número de instâncias no Render (Scale Out).
2. Aumentar `WEB_CONCURRENCY` (Scale Up) se houver CPU sobrando.

### Nível 2: Banco de Dados (Stateful)
O gargalo primário é o número de conexões.
1. **Atual:** Neon com PgBouncer (Pool Size 20/worker).
2. **Expansão:** Aumentar Compute Unit no Neon (Autoscaling).
3. **Otimização:** Aumentar TTL de Cache no Redis para rotas de leitura (`/menu`).

## 4. Plano de Teste de Carga
Executar `scripts/production/run_load_test.py` antes de grandes eventos (Black Friday, Dia das Mães).

**Cenário Padrão:**
- 50 Usuários simultâneos.
- Ramp-up de 10 usuários/segundo.
- Duração de 1 minuto.
- Foco: Criação de Pedidos e Dashboard.
