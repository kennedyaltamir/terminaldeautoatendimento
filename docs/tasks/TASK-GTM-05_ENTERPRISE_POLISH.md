# DOMAIN: LEGAL_COMPLIANCE
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-05
TITLE: Enterprise Polish (RoPA, Store Safety & SLA)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema possui Termos de Uso e Política de Privacidade básicos.
- Faltam artefatos específicos exigidos por auditorias LGPD rigorosas (RoPA, Política de Retenção).
- Faltam documentos de suporte para preenchimento dos formulários de segurança das Lojas (Google Play Data Safety / Apple Privacy Nutrition Label).
- Faltam documentos de nível Enterprise (SLA, Security Policy).

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Compliance LGPD elevado para 10/10 com Registro de Operações (RoPA) e Política de Retenção explícita.
- Documentação pronta para "copiar e colar" nos formulários das Stores.
- Repositório com postura de "Vendor Enterprise" (SECURITY.md, SLA.md).
- Script de validação confirmando a existência de todos os artefatos de governança.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação de `docs/legal/RoPA.md` (Registro de Operações).
- Atualização de `docs/legal/PRIVACY_POLICY.md` com seção de Retenção e Descarte.
- Criação de `docs/legal/STORE_DATA_SAFETY.md` (Guia para Stores).
- Criação de `SECURITY.md` (Divulgação de Vulnerabilidades).
- Criação de `docs/legal/SLA.md` (Acordo de Nível de Serviço).
- Script de validação `scripts/production/verify_enterprise_readiness.py`.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Implementação técnica de exclusão automática (o foco é a política/documento).
- Preenchimento manual nos portais da Apple/Google (apenas o guia é gerado).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Idioma: Português Brasil.
- Formato: Markdown estrito.
- Conformidade: LGPD (Lei 13.709/2018).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `docs/legal/PRIVACY_POLICY.md` existente.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- 5 Novos arquivos de documentação legal/compliance.
- 1 Arquivo atualizado (Privacy Policy).
- 1 Script de validação.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] RoPA lista categorias de dados, finalidade e base legal.
- [x] Política de Privacidade contém seção explícita sobre prazos de retenção.
- [x] Guia de Store Safety cobre Android e iOS.
- [x] SECURITY.md define canal de denúncia.
- [x] SLA define uptime alvo e janelas de manutenção.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_enterprise_readiness.py`
RESULTADO_ESPERADO: "Enterprise Readiness Check Passed: 10/10 Compliance."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover arquivos criados em `docs/legal/`.
- Reverter `docs/legal/PRIVACY_POLICY.md`.