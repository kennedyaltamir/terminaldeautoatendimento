# DOMAIN: DEVOPS
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-OPS-05
TITLE: CI/CD Pipeline Hardening (Governance Gates & Policy-as-Code)
OWNER: Executor Kernel
PRIORITY: ALTA (QUALITY ASSURANCE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O projeto possui diversos scripts de verificação de governança (`verify_adr_integrity.py`, `verify_compliance_mapping.py`, etc.) criados nas tasks anteriores.
- Esses scripts são executados manualmente. Se um desenvolvedor commitar uma alteração que quebre a integridade da documentação (ex: apagar uma ADR), o erro passará despercebido até uma auditoria manual.
- O pipeline atual (`.github/workflows/ci.yml`) foca apenas em testes unitários e build do frontend.
- Clientes Enterprise exigem garantia de que as políticas de segurança e governança são aplicadas automaticamente ("Policy as Code").

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O pipeline de CI/CD (`ci.yml`) inclui um job dedicado de **Governança e Compliance**.
- O build falha automaticamente se:
    - Uma ADR estiver malformada ou faltando.
    - O mapeamento de compliance apontar para evidências inexistentes.
    - A lista de fornecedores estiver inconsistente.
    - O Trust Center estiver desconfigurado.
- A integridade da documentação Enterprise é tratada com a mesma criticidade que o código-fonte.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Atualização do `.github/workflows/ci.yml` para incluir os steps de validação de governança.
- Criação de script de validação do próprio CI (`scripts/production/verify_ci_readiness.py`) para garantir que as regras estão configuradas.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Implementação de deploy contínuo (CD) para produção (o foco é a validação/CI).
- Configuração de runners self-hosted.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Formato: GitHub Actions YAML.
- Os scripts de governança devem rodar em ambiente Linux (Ubuntu-latest) no CI.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `.github/workflows/ci.yml` existente.
- Scripts de verificação em `scripts/production/`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `.github/workflows/ci.yml` (Atualizado).
- `scripts/production/verify_ci_readiness.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] O arquivo YAML contém um job ou steps para `Governance Checks`.
- [x] Os scripts `verify_adr_integrity.py`, `verify_compliance_mapping.py`, `verify_vendor_risk.py` e `verify_trust_center.py` são chamados.
- [x] O script de validação confirma que o CI está configurado para rodar essas verificações.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_ci_readiness.py`
RESULTADO_ESPERADO: "CI/CD Hardening Verified: Governance Gates are active."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `.github/workflows/ci.yml` para a versão anterior.
