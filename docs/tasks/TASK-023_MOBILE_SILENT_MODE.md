# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-023
TITLE: Implementar Controles de Modo Silencioso e Gestão de Alertas no KDS
OWNER: Executor Kernel
PRIORITY: ALTA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O KDS Mobile dispara vibrações físicas via `AlertsOutputService` sempre que um pedido atinge estado CRITICAL ou BREACHED.
- Não existe mecanismo de persistência para preferências do usuário local.
- Não existe interface gráfica para desativar os alertas sonoros/físicos.
- A lógica de disparo é direta: `Engine -> Output`.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O aplicativo possui uma `SettingsStore` persistida (AsyncStorage) que armazena `isSilentMode` (boolean).
- A interface do KDS (`OrdersScreen`) exibe um botão de toggle (Sino Ativo/Inativo) no header.
- O `AlertsOutputService` consulta a `SettingsStore` antes de executar qualquer efeito físico.
- Se `isSilentMode` for true, nenhuma vibração ou som é emitido, independentemente do SLA.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação de `mobile/src/store/settings.store.ts` com Zustand + Persist Middleware.
- Modificação de `mobile/src/services/alerts/alerts.output.service.ts` para ler a store.
- Adição de botão de controle na `mobile/src/screens/orders/OrdersScreen.tsx`.
- Definição de ícones `Bell` e `BellOff` (Lucide React Native).

### EXCLUI
- Configurações de servidor (backend).
- Perfis de alerta por usuário (a configuração é por dispositivo).
- Alteração na lógica de cálculo de SLA (apenas na saída do alerta).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Linguagem: TypeScript.
- State Management: Zustand.
- Persistência: `@react-native-async-storage/async-storage`.
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Biblioteca `lucide-react-native` já instalada.
- `AlertsOutputService` existente.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivo `mobile/src/store/settings.store.ts`.
- Arquivo `mobile/src/services/alerts/alerts.output.service.ts` modificado.
- Arquivo `mobile/src/screens/orders/OrdersScreen.tsx` modificado.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O estado `isSilentMode` persiste após fechar e abrir o app.
- [ ] O ícone muda visualmente entre `Bell` e `BellOff` ao clicar.
- [ ] Quando `isSilentMode = true`, a função `Vibration.vibrate` NÃO é chamada mesmo com pedidos atrasados.
- [ ] Quando `isSilentMode = false`, a vibração ocorre normalmente.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: Teste Manual via Expo Go.
RESULTADO_ESPERADO:
1. Ativar modo silencioso.
2. Forçar estado BREACHED em um pedido (mock).
3. O dispositivo NÃO deve vibrar.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover `SettingsStore`.
- Reverter `AlertsOutputService` para disparar incondicionalmente.
- Remover botão da UI.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO criar configurações que dependam de chamada de API.
- É PROIBIDO usar Context API (usar Zustand).
