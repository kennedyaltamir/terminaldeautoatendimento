# DOMAIN: SECURITY
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-SEC-02
TITLE: Automated Dependency Security Audit (SCA)
OWNER: Executor Kernel
PRIORITY: ALTA (SECURITY / COMPLIANCE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O MesaFlow possui controles de segurança de aplicação (SAST) e infraestrutura.
- No entanto, não há verificação automatizada de vulnerabilidades em bibliotecas de terceiros (Software Composition Analysis - SCA).
- Dependências desatualizadas ou vulneráveis (ex: `requests`, `next`, `react`) podem introduzir riscos críticos (CVEs) mesmo que o código proprietário seja seguro.
- Auditorias Enterprise (ISO 27001 A.12.6.1) exigem gestão técnica de vulnerabilidades.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de varredura automática de dependências para Backend (Python) e Frontend/Mobile (Node.js).
- Utilização de ferramentas padrão de mercado: `pip-audit` (Python) e `npm audit` (Node).
- Script unificado `scripts/security/audit_dependencies.py` que executa as verificações e reporta falhas.
- Bloqueio de deploy em caso de vulnerabilidades críticas conhecidas.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Adição de `pip-audit` ao `requirements.txt`.
- Criação do script de auditoria unificado.
- Execução de auditoria no Backend (`requirements.txt`).
- Execução de auditoria no Frontend (`frontend/package.json`).
- Execução de auditoria no Mobile (`mobile/package.json`).
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Correção automática de versões (o script apenas reporta).
- Auditoria de containers Docker (trivy/grype) - foco em dependências de aplicação.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Ferramentas: `pip-audit` (PyPI), `npm audit` (NPM).
- Saída: Relatório textual no terminal com Exit Code.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `requirements.txt`
- `frontend/package.json`
- `mobile/package.json`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `requirements.txt` (Atualizado).
- `scripts/security/audit_dependencies.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Script identifica vulnerabilidades em pacotes Python.
- [x] Script identifica vulnerabilidades em pacotes Node.js.
- [x] Script retorna erro se encontrar vulnerabilidades de alta severidade (simulado ou real).
- [x] Ferramenta `pip-audit` instalada no ambiente.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/security/audit_dependencies.py`
RESULTADO_ESPERADO: "SCA Audit Completed." (Pode conter avisos de vulnerabilidades reais, o que é esperado e desejado).

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover `pip-audit` de `requirements.txt`.
- Remover `scripts/security/audit_dependencies.py`.
