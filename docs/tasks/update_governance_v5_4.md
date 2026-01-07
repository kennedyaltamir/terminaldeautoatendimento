# Task: Atualização de Governança v5.4 (Endurecimento de Protocolo)

## Contexto
Identificada necessidade de mitigar riscos de alucinação de progresso e desvio de escopo durante a transferência entre instâncias de IA.

## Decisões Técnicas
- **Double-Lock de Papel:** Executor agora possui inteligência crítica (alerta) mas zero autonomia de mudança de escopo.
- **Anti-Scope Creep:** Introduzida a Regra R6 para proibir melhorias implícitas.
- **Validação Semântica de Domínio:** Introduzida a Regra R7 para garantir isolamento.
- **Correção de Status:** Retificada a informação sobre a Missão 14A (Auth Semântica), que permanece aberta.

## Arquivos Afetados
- `docs/Prompts/System_Instructions.xml`
- `docs/Prompts/Master_Handover_Executor.xml`

## Política de Testes
[TEST_EXEMPT: Alteração de meta-instruções de governança.]
