
# RFC: Script Organization Standard
**Status:** ACTIVE
**Domain:** GOVERNANCE / DEVOPS
**Date:** 2026-01-13

## 1. Motivação
A estrutura de scripts do projeto apresentava redundância e dispersão. Para atingir a maturidade L6, é imperativo que cada ferramenta resida em um domínio funcional único.

## 2. Nova Estrutura Canônica
Fica estabelecido que todos os scripts devem residir em `/scripts/` sob a seguinte taxonomia:

- **automation/**: Bots, IA Ops e QA reativo.
- **ci_cd/**: Automação de pipeline e gates.
- **governance/**: Selagem e auditoria constitucional.
- **maintenance/**: Saúde sistêmica e higiene de contexto.
- **migrations/**: Banco de dados, schema e RLS.
- **observability/**: Probes, healthchecks e telemetria.
- **security/**:Boundary audit e pentest.
- **setup/**: Bootstrap de infra e ambiente.
- **validation/**: Provas de trabalho e readiness.
- **verification/**: Integridade cruzada profunda.
- **release/**: Ops de lançamento e rollback.
- **tests_support/**: Utilitários para suítes de teste.
- **mobile/**: Específicos do ambiente nativo.
- **_archive/**: Obsoletos e legados.

## 3. Regras de Manutenção
1. **Unicidade**: Um script só pode existir em UM domínio funcional.
2. **Hierarquia SSOT**: Toda organização de scripts deve estar alinhada ao `/MASTER_PROJECT_SPECIFICATION.md`, que prevalece sobre qualquer RFC ou diretriz local.
3. **Registro**: Inclusões devem ser refletidas no `SCRIPT_REGISTRY.json`.
4. **Imports**: Scripts devem usar paths relativos à raiz do projeto.

---
*Aprovado por Architect Kernel L6.*

