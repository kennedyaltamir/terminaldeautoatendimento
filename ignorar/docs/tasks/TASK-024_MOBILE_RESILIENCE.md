# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-024
TITLE: Implementar Resiliência de Rede com Backoff Exponencial e Reconciliação de Estado
OWNER: Executor Kernel
PRIORITY: CRÍTICA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O WebSocket tenta conectar uma vez. Se falhar, ou se a conexão cair, o comportamento de reconexão é básico ou inexistente.
- Não existe garantia de que o estado local (lista de pedidos) esteja sincronizado após uma reconexão (gap de eventos).
- O usuário não recebe feedback visual claro de "Sincronizando".

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O sistema implementa uma estratégia de `Exponential Backoff` para reconexão do WebSocket (2s, 4s, 8s, 16s, 30s).
- Ao restabelecer a conexão (`onopen`), o sistema dispara automaticamente um `Full Sync` (GET /orders) para reconciliar o estado.
- A UI exibe um indicador discreto de "Sincronizando" durante o processo de reconciliação.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação de `mobile/src/services/realtime.reconnect.policy.ts`.
- Atualização de `mobile/src/services/orders.realtime.service.ts` para usar a política de backoff.
- Atualização de `mobile/src/services/orders.sync.service.ts` para expor método de reconciliação.
- Integração do evento de reconexão com o disparo do sync.

### EXCLUI
- Cache offline de pedidos (persistência local é outra task).
- Alterações no Backend.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Linguagem: TypeScript.
- Lógica de Tempo: `setTimeout` gerenciado.
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `OrdersRealtimeService` existente.
- `OrdersService` (API REST) existente.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivo `mobile/src/services/realtime.reconnect.policy.ts`.
- Arquivo `mobile/src/services/orders.realtime.service.ts` atualizado.
- Arquivo `mobile/src/store/orders.store.ts` atualizado (flag `isSyncing`).

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O socket tenta reconectar automaticamente após queda, com intervalos crescentes.
- [ ] O limite máximo de intervalo é respeitado (ex: 30s).
- [ ] Um `GET /orders` é disparado imediatamente após o evento `socket.onopen` (se for uma reconexão).
- [ ] A flag `isSyncing` na store fica `true` durante a reconciliação e `false` ao terminar.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: Teste Manual (Modo Avião).
RESULTADO_ESPERADO:
1. Cortar internet.
2. Logs mostram tentativas de reconexão espaçadas.
3. Voltar internet.
4. Log mostra "Reconnected" seguido de "Full Sync Completed".

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `OrdersRealtimeService` para lógica simples.
- Remover arquivo de política de reconexão.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO fazer "polling" (chamadas REST repetidas) como substituto do WebSocket. O REST é apenas para reconciliação pontual.
