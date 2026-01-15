
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 11:45:00
# 📜 Governance Changelog
**Data:** 13/01/2026
**Status:** ATIVO

## Registro de Overrides e Decisões
Este documento substitui o uso da tag `<Governance_Override>` no `registry.xml`, centralizando justificativas de alterações sensíveis conforme Protocolo INDA V10.

### 1. Ajuste de Status de Scripts (13/01/2026)
- **Ação:** Depreciação de scripts de automação visual (`MAP-ROUTES`, `ENTERPRISE-UI-E`, `AUDIT-SCRIPT-IN`).
- **Motivo:** Foco em testes funcionais de backend e segurança. Scripts puramente visuais ou de inventário foram removidos fisicamente pelo `janitor_governance.py`.
- **Impacto:** O Registry agora reflete apenas a infraestrutura ativa.

### 2. Inclusão de SYS-01
- **Ação:** Registro do `system_integrity_check.py` como `SYS-01`.
- **Estado Inicial:** `PENDING`.
- **Motivo:** Novo script canônico de auditoria de integridade (Read-Only).

### 3. Correção de Paths no Master Readiness
- **Ação:** Atualização dos caminhos no `master_readiness_check.py`.
- **Motivo:** Scripts foram movidos de `maintenance/` para `validar/` pela rotina de organização, quebrando o pipeline de verificação.

