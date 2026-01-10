# DOMAIN: MOBILE / DEVOPS
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-09
TITLE: Mobile OTA Updates (Expo Updates) & Code Push
OWNER: Executor Kernel
PRIORITY: CRÍTICA (MAINTENANCE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O app mobile depende de submissão completa às lojas para qualquer correção de bug em JS/Assets.
- O ciclo de aprovação da Apple/Google (24h-72h) é incompatível com a agilidade necessária em GTM.
- Não há mecanismo de "Hotfix" em tempo real.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Configuração completa do `expo-updates`.
- Implementação de política de atualização obrigatória para versões críticas.
- Pipeline de deploy configurado para `eas update`.
- O app verifica e baixa novas versões silenciosamente em background.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Configuração do `app.json` (runtimeVersion, updates).
- Implementação de UI de "Baixando Atualização" (opcional/discreta).
- Separação de canais (production, preview).

### EXCLUI
- Atualizações de código nativo (que exigem novo build).

✅ 5. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
- [ ] Comando `eas update` reflete no app sem reinstalação.
- [ ] O app identifica a versão do bundle no menu de ajuda.
