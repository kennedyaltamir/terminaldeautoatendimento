# 🏛️ Governança Autônoma L10.2: Rastreabilidade e Versionamento
**Versão:** 10.0.2-AUTO | **Domínio:** GOVERNANCE | **Status:** ENFORCED

## 1. Geração Automática de ADRs
- **Trigger:** Quando uma task no `TASKS.md` contém a tag `[ARCH]`, o `atualizar.py` invoca um script que gera um template de ADR (`ADR-XXX.md`) em `docs/decisions/`.
- **Integridade:** O template inclui um placeholder `integrity_hash` que deve ser preenchido com o SHA256 do commit que implementa a decisão.

## 2. Rastreabilidade de Ciclos Autônomos
Cada execução do `atualizar.py` gera um **Manifesto de Ciclo** em `governance/evidence/cycles/`:
```json
{
  "cycle_id": "2c29f520",
  "version": "10.0.2-AUTO",
  "timestamp": "...",
  "task_id": "TASK-SRE-05",
  "adr_link": "ADR-005.md",
  "commit_hash": "a1b2c3d4...",
  "verification_script": "l10_autonomous_gate.py",
  "verdict": "SUCCESS"
}
```
Isso cria uma cadeia de custódia inquebrável entre a decisão, a implementação e a validação.