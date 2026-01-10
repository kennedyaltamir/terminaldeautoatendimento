# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-036
TITLE: Executar e Validar Build Nativo de Produção (Release Candidate)
OWNER: Executor Kernel
PRIORITY: CRÍTICA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O projeto roda em modo gerenciado (Expo Go) ou Dev Client.
- `eas.json` está configurado preliminarmente.
- `app.json` possui metadados básicos.
- Não existe um binário `.apk` (Android) ou `.ipa` (iOS) de produção gerado e validado.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O projeto compila com sucesso no EAS Build (perfil `preview` ou `production`).
- Um arquivo `.apk` instalável é gerado.
- O aplicativo instalado abre, conecta na API de produção e realiza login sem erros de crash nativo.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Revisão final de `mobile/app.json` (Package name, version, icon, splash).
- Revisão de `mobile/eas.json`.
- Execução do comando de build local ou nuvem (`eas build --platform android --profile preview --local` ou cloud).
- Resolução de conflitos de dependências nativas (Gradle/Podfile).

### EXCLUI
- Publicação nas lojas (Google Play / App Store).
- Configuração de Apple Developer Account (foco inicial em Android APK).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Ferramenta: EAS CLI.
- Plataforma Alvo: Android (APK).
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Código fonte atual.
- Credenciais Expo (configuradas no ambiente).

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivo binário `.apk` (ou link para download).
- Log de sucesso do build.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O comando `eas build` termina com status "Finished".
- [ ] O APK pode ser instalado em um emulador ou dispositivo físico.
- [ ] O app não fecha (crash) ao abrir (Splash Screen -> Login).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `eas build --platform android --profile preview --local` (ou cloud).
RESULTADO_ESPERADO: "Build successful".

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter alterações em `app.json` ou `package.json` feitas para acomodar o build.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO commitar chaves de assinatura (Keystore) no repositório. Elas devem ser gerenciadas pelo EAS.
