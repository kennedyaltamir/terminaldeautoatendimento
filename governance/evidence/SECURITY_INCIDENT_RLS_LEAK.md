
# RELATÓRIO DE INCIDENTE DE SEGURANÇA: RLS LEAK
**ID:** INC-SEC-20260112-002
**Data:** 12/01/2026
**Status:** OPEN (BLOQUEANTE)
**Severidade:** CRÍTICA (DATA BREACH RISK)

## 1. Descrição do Incidente
O script de validação de segurança (`verify_TASK-SEC-01.py`) detectou uma falha crítica no isolamento multi-tenant. Um tenant (B) conseguiu ler dados pertencentes a outro tenant (A) através de uma query padrão do ORM, indicando que o Row-Level Security (RLS) não está ativo ou não está sendo aplicado corretamente.

## 2. Evidência Técnica
- **Script Executor:** `scripts/validation/verify_TASK-SEC-01.py`
- **Objeto Vazado:** Order ID `49122b52-1703-44e4-922f-93f92920c76c`
- **Cenário:**
    1.  Tenant A criou o pedido.
    2.  Sessão trocou contexto para Tenant B (`set_tenant`).
    3.  Tenant B executou `db.query(Order).filter(Order.id == order_a.id).first()`.
    4.  **Resultado Esperado:** `None` (Bloqueio pelo Banco).
    5.  **Resultado Obtido:** Objeto Order (Vazamento).

## 3. Impacto de Negócio
- **Bloqueio de Venda:** O sistema não pode ser comercializado ou colocado em produção.
- **Risco Legal:** Violação direta da LGPD e contratos de confidencialidade B2B.
- **Integridade:** A arquitetura "Zero Trust" baseada em banco de dados falhou.

## 4. Ação Imediata
- **Status:** Investigação em curso.
- **Próximo Passo:** Execução de diagnóstico profundo (`inspect_rls_context.py`) para identificar a causa raiz (Configuração de Banco vs Propagação de Sessão).


