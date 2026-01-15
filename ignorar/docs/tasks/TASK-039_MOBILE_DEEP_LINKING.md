# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-039
TITLE: Implementar Deep Linking Universal para Abertura de Mesas via QR Code
OWNER: Executor Kernel
PRIORITY: MÉDIA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O app abre apenas na tela inicial.
- QR Codes de mesa abrem o PWA (Web) por padrão.
- Não existe configuração de `scheme` ou `linking` no React Navigation.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O app responde ao esquema `mesaflow://`.
- A URL `mesaflow://table/{id}?code={token}` abre diretamente a tela de detalhes da mesa ou inicia o fluxo de check-in no app nativo.
- Se o usuário não estiver logado, redireciona para Login e depois retoma a ação.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Configuração de `scheme` em `mobile/app.json`.
- Configuração do objeto `linking` no `NavigationContainer` (`mobile/src/navigation/RootNavigator.tsx`).
- Tratamento de parâmetros de rota na `WaiterTablesScreen` ou `OrderEntryScreen`.

### EXCLUI
- Universal Links (HTTPS) - Foco apenas em Custom Scheme neste momento.
- Alteração nos QR Codes impressos (eles continuarão apontando para Web, o Deep Link é para uso interno ou futuro).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: React Navigation v6/v7.
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Estrutura de navegação atual.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `mobile/app.json` atualizado.
- `mobile/src/navigation/linking.ts` (Novo arquivo de configuração).
- `mobile/src/navigation/RootNavigator.tsx` atualizado.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O comando `npx uri-scheme open mesaflow://table/1` abre o app.
- [ ] O app navega para a tela correta baseada na URL.
- [ ] Parâmetros da URL são extraídos corretamente.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `npx uri-scheme open mesaflow://table/1 --android`
RESULTADO_ESPERADO: O emulador abre o app e navega para a mesa 1.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover configuração de `linking` do NavigationContainer.
- Remover `scheme` do `app.json`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO quebrar a navegação padrão manual.
