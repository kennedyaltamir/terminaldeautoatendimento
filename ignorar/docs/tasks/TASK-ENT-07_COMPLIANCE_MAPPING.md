# DOMAIN: GOVERNANCE
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-ENT-07
TITLE: Compliance Control Mapping (SOC2 & ISO 27001 Alignment)
OWNER: Executor Kernel
PRIORITY: ALTA (AUDIT READINESS)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O MesaFlow implementou diversos controles de segurança e governança (RLS, Logs, Policies, Vendor Risk).
- No entanto, esses controles estão descritos em linguagem técnica ou de produto.
- Auditores externos e equipes de GRC (Governance, Risk, and Compliance) de clientes Enterprise exigem um "De/Para" que mapeie funcionalidades do sistema para controles normativos padrão (SOC2 TSC ou ISO 27001 Annex A).
- A falta desse mapeamento obriga o preenchimento manual e repetitivo de planilhas de segurança.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Criação do `docs/enterprise/COMPLIANCE_MAPPING.md`: Uma matriz de rastreabilidade que conecta controles do MesaFlow a requisitos de mercado.
- O documento deve cobrir: Acesso Lógico, Operações, Gestão de Mudança e Proteção de Dados.
- Script de validação para garantir que todos os controles citados possuem evidência documental no repositório.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Mapeamento de controles para SOC 2 (Security, Availability, Confidentiality).
- Mapeamento de controles para ISO 27001 (A.5 a A.18).
- Referência direta aos arquivos de evidência (`EVIDENCE_PACK`, `SECURITY_POLICY`, etc.).
- Script `scripts/production/verify_compliance_mapping.py`.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Contratação de auditoria (AICPA/ISO).
- Implementação de controles físicos (Datacenter).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Padrão: AICPA SOC 2 (2017 criteria) e ISO/IEC 27001:2013/2022.
- Formato: Tabela Markdown.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Todos os documentos gerados nas tasks ENT-01 a ENT-06.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `docs/enterprise/COMPLIANCE_MAPPING.md`
- `scripts/production/verify_compliance_mapping.py`

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Matriz cobre pelo menos 10 controles críticos do SOC 2 (CC series).
- [x] Matriz cobre controles de Criptografia e Acesso da ISO 27001.
- [x] Cada controle mapeado aponta para um arquivo existente no repo.
- [x] Script de validação confirma a integridade dos links de evidência.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_compliance_mapping.py`
RESULTADO_ESPERADO: "Compliance Mapping Verified: Controls linked to valid evidence."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover `docs/enterprise/COMPLIANCE_MAPPING.md`.
