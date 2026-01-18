# 📋 Padronização e Templates de Governança
**Versão:** 5.0.1-SEQ | **Domínio:** GOVERNANCE

## 1. Padrão de Nomenclatura e Versão
- **Documentos:** `v<MAJOR>.<MINOR>.<PATCH>-<TYPE>`
    - `SEQ`: Sequencial/Auditável.
    - `FIX`: Hotfix Documental.
    - `ADR`: Architecture Decision.
- **Scripts:** `scripts/<domain>/<id>_<name>.py` (ex: `scripts/security/sec_01_rls_integrity.py`).

## 2. Template: Architecture Decision Record (ADR)
```markdown
# ADR-[ID]: [Título Curto]
**Data:** YYYY-MM-DD | **Status:** [PROPOSED | ACCEPTED | SUPERSEDED]
**Contexto:** [O problema que estamos resolvendo]
**Decisão:** [A solução técnica escolhida]
**Consequências:** [Prós e Contras]
**Rastreabilidade:** [Link para SDS ou Task]
**Integridade:** HASH_SHA256_AQUI
```

## 3. Checklist de Pré-Deploy (Compliance Gate)
- [ ] **SEC:** `sec_04_env_audit.py` retorna SUCCESS.
- [ ] **FIN:** `test_ledger_integrity.py` retorna SUCCESS.
- [ ] **QA:** `enterprise_delivery_l8.py` (Full Loop) retorna SUCCESS.
- [ ] **GOV:** `registry.xml` sincronizado e sem bloqueios.
- [ ] **LEGAL:** Termos de Uso e Privacidade atualizados em `/trust`.