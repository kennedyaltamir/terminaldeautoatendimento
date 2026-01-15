# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-MOB-01
TITLE: Otimizar Global Clock para Economia de Energia
OWNER: Executor Kernel
PRIORITY: MÉDIA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O `GlobalClockService.ts` mantém um `setInterval` ativo a cada 5 segundos para processar SLAs e alertas.
- Este timer permanece ativo mesmo quando o aplicativo é minimizado ou o dispositivo entra em modo de repouso.
- Observou-se um consumo de bateria desproporcional em turnos longos de operação.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O `GlobalClockService` é consciente do estado do aplicativo (`AppState`).
- O timer é automaticamente pausado (`clearInterval`) quando o app entra em `background` ou `inactive`.
- O timer é reiniciado imediatamente com um pulso de sincronização assim que o app volta para `active`.
- Redução drástica do uso de CPU em background.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Implementação do listener de `AppState` no `GlobalClockService`.
- Lógica de gerenciamento de ciclo de vida do intervalo.
### EXCLUI
- Alteração na frequência do pulso (mantém-se 5s para o modo ativo).
- Alterações na lógica de cálculo de SLA.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: React Native / Expo.
- API Nativa: `AppState`.
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Arquivo `mobile/src/services/global.clock.service.ts`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivo `global.clock.service.ts` atualizado.
- Script de validação `scripts/validation/verify_TASK-MOB-01.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O timer é destruído ao minimizar o app (verificado via logs).
- [ ] O timer é recriado ao maximizar o app.
- [ ] Um pulso de tempo é emitido no exato momento do retorno ao primeiro plano.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `adb logcat | grep "[Clock]"`
RESULTADO_ESPERADO: Logs de "Pausado" e "Reiniciado" conforme a interação com o app.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter para a versão do Clock que ignora o estado do sistema.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO manter qualquer processamento de reordenação de lista enquanto o app estiver em background.
