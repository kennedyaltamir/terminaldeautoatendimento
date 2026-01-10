# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-03
TITLE: Build Mobile de Produção (Publicação em Lojas)
OWNER: Executor Kernel
PRIORITY: ALTA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O projeto mobile está configurado para builds de desenvolvimento (`apk`) e preview.
- O arquivo `eas.json` carece de um perfil de produção explícito para geração de `.aab` (Android App Bundle) e `.ipa` (iOS Store).
- Não há validação automatizada dos metadados de versão (`versionCode`, `buildNumber`) necessários para submissão nas lojas.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- `mobile/eas.json` configurado com perfil `production` otimizado para Google Play e App Store.
- `mobile/app.json` validado com identificadores de pacote e versionamento semântico.
- Script de verificação `scripts/production/verify_mobile_build.py` garantindo que o ambiente está pronto para o comando `eas build`.
- Definição clara das variáveis de ambiente de produção (`API_URL`, `APP_ENV`).

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Configuração do perfil `production` no EAS Build.
- Definição de `buildType: app-bundle` para Android.
- Definição de `distribution: store` para iOS.
- Script de validação de pré-requisitos de loja.

### EXCLUI
- Execução do build na nuvem (comando `eas build` real consome créditos e tempo).
- Upload manual para os consoles da Apple/Google.
- Geração de certificados (gerenciados pelo EAS Credentials).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Ferramenta: EAS CLI (Expo Application Services).
- Formatos: `.aab` (Android), `.ipa` (iOS).
- Canal de Update: `production`.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `mobile/eas.json`
- `mobile/app.json`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `mobile/eas.json` atualizado.
- `scripts/production/verify_mobile_build.py`.
- Atualização do `docs/TASKS.md`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Perfil `production` existe em `eas.json`.
- [x] Android está configurado para gerar `app-bundle`.
- [x] iOS está configurado para distribuição `store`.
- [x] Script de validação confirma presença de `package` e `bundleIdentifier`.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_mobile_build.py`
RESULTADO_ESPERADO: "Mobile Build Config Verified: READY FOR STORE SUBMISSION."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `mobile/eas.json` para versão anterior.