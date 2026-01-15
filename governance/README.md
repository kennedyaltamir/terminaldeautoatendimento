
# 🏛️ MesaFlow Governance Center (L6)

Este diretório é a **Fonte de Verdade (SSOT)** para o estado de prontidão do sistema. 

## ⚠️ Conditional Production Readiness
Atualmente, o sistema encontra-se em estado **PRODUCTION_READY_CONDITIONAL**.
Isso significa que a arquitetura lógica e os controles de segurança estão validados, porém dependências operacionais externas impedem o Go-Live completo.

### Bloqueios Ativos para Deploy:
1. **SEC-04 (Environment):** O arquivo `.env` local utiliza mocks ou possui chaves ausentes. O sistema bloqueia o avanço para produção sem chaves reais de integração (Stripe/MP).
2. **INF-01 (Connectivity):** O Healthcheck falhou no último rito porque o serviço API não estava respondendo no momento da verificação.
3. **SEC-01 (RLS):** Em fase de re-validação para garantir que a migração de diretórios não afetou a carga das políticas SQL.

## 🕵️ Fluxo de Auditoria
O auditor deve:
1. Consultar `registry.xml` para ver os Quality Gates.
2. Validar relatórios técnicos em `/governance/evidence/`.
3. Validar normas em `/governance/policies/`.

---
**ESTADO ATUAL: AUDIT-READY (CONDITIONAL) | GO-LIVE: BLOCKED**

