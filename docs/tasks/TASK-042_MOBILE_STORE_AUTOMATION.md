# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-042
TITLE: Automatizar Geração de Screenshots e Metadados para Lojas
OWNER: Executor Kernel
PRIORITY: MÉDIA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- A geração de screenshots para Google Play e App Store é manual.
- Não existe padronização de tamanho ou dispositivo para as capturas.
- O processo de release consome tempo excessivo na preparação de ativos de marketing.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Existe uma configuração básica de `fastlane` no projeto mobile.
- Um `Snapfile` (ou script equivalente) define os dispositivos e idiomas alvo.
- Um comando único gera screenshots das telas principais (Login, KDS, Mesas).

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Inicialização do Fastlane no diretório `mobile/`.
- Criação de `mobile/fastlane/Fastfile` e `mobile/fastlane/Snapfile`.
- Configuração de uma lane `screenshots` que executa testes de UI para captura (usando Detox ou script nativo se configurado, ou apenas estrutura de pastas se não houver testes de UI prontos).
- *Nota:* Como não temos Detox configurado, esta task focará na **Estrutura do Fastlane** e um script placeholder de captura via ADB (Android) para automação inicial.

### EXCLUI
- Configuração de deploy automático (apenas screenshots).
- Criação de testes E2E complexos (apenas navegação básica para print).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Ferramenta: Fastlane.
- Plataforma: Android (Prioritário).
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Acesso ao ambiente de desenvolvimento.
- `adb` configurado.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Pasta `mobile/fastlane/`.
- Arquivo `mobile/fastlane/Fastfile`.
- Script `scripts/automation/capture_mobile_screens.py` (Wrapper para ADB screencap).

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Fastlane instalado e inicializado.
- [ ] Script de captura Python executa comandos ADB e salva arquivos na pasta `docs/screenshots/mobile`.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/automation/capture_mobile_screens.py`
RESULTADO_ESPERADO: Screenshots salvas na pasta de destino.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover pasta `mobile/fastlane`.
- Remover script de automação.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO commitar credenciais da Apple/Google no repositório (usar variáveis de ambiente).
