# ADR-004: Estratégia de Dual Health Endpoint

**Status:** ACEITA
**Data:** Janeiro de 2026
**Decisores:** Architect Kernel

## Contexto
O sistema precisa ser monitorado por ferramentas externas (Load Balancers, UptimeRobot, Status Pages) que, por padrão, buscam o endpoint `/health` na raiz. A arquitetura original expunha apenas `/api/health`.

## Decisão
Implementar **Dual Binding** para o Health Check, expondo a mesma lógica de verificação em duas rotas: `/health` (Raiz) e `/api/health` (Namespace API).

## Alternativas Consideradas

### 1. Redirecionamento (307 Redirect)
- **Descrição:** `/health` redireciona para `/api/health`.
- **Contras:** Alguns Load Balancers não seguem redirects, interpretando 3xx como falha. Aumenta latência.
- **Motivo do Descarte:** Risco de falso positivo em monitoramento.

### 2. Manter apenas `/api/health`
- **Descrição:** Forçar todos os clientes a usarem o path da API.
- **Contras:** Quebra convenções de mercado e ferramentas "opinionated" que não permitem configurar path.
- **Motivo do Descarte:** Fricção desnecessária com ferramentas Enterprise.

## Consequências

### Positivas
- **Compatibilidade:** Funciona com qualquer ferramenta de monitoramento padrão.
- **Resiliência:** Permite verificação de saúde mesmo se o roteador `/api` tiver problemas de montagem.
- **Simplicidade:** Implementação via decorator stacking no FastAPI, sem duplicação de código lógico.

### Negativas
- **Poluição de Rota:** Exposição de rota na raiz (mitigado por `include_in_schema=False` no Swagger).

## Compliance
Facilita a auditoria de disponibilidade e SLA, permitindo monitoramento externo transparente.