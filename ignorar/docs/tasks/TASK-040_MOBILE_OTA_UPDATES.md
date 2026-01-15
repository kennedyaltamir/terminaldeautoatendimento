# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-040
TITLE: Configurar Pipeline de Atualizações Over-The-Air (OTA) via Expo Updates
OWNER: Executor Kernel
PRIORITY: MÉDIA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- Qualquer alteração de código JS/TS exige um novo build nativo (.apk) e reinstalação.
- O pacote `expo-updates` não está configurado ou inicializado.
- Não existe canal de release definido (`preview`, `production`).

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O aplicativo verifica atualizações de JS na inicialização.
- É possível enviar correções de bugs (hotfixes) via comando `eas update` sem gerar novo binário.
- O `app.json` contém a configuração correta de `updates`.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Instalação de `expo-updates`.
- Configuração de `updates.url` e `updates.fallbackToCacheTimeout` em `app.json`.
- Definição de canais no `eas.json`.
- Teste de fluxo de update.

### EXCLUI
- Atualizações que envolvam código nativo (novas bibliotecas com linking).
- Configuração de servidor de updates próprio (usaremos EAS).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Serviço: EAS Update.
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Projeto Expo configurado com EAS.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `mobile/app.json` atualizado.
- `mobile/eas.json` atualizado.
- `mobile/package.json` atualizado.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O app inicia sem erros após a instalação da lib.
- [ ] O comando `eas update` executa com sucesso.
- [ ] O app baixa o novo bundle e reinicia com as alterações.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO:
1. Buildar APK (Preview).
2. Instalar.
3. Mudar cor de um botão.
4. `eas update --branch preview`.
5. Abrir app 2 vezes.
RESULTADO_ESPERADO: A cor do botão muda na segunda abertura.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover `expo-updates`.
- Reverter `app.json`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO configurar updates para bloquear a inicialização por mais de 5 segundos (fallback obrigatório).
