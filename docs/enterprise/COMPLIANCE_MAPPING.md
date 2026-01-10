# 🏛️ Matriz de Mapeamento de Compliance (SOC2 & ISO 27001)

**Versão:** 1.1 (Path Fix)
**Status:** AUDIT READY
**Escopo:** MesaFlow SaaS Platform

Este documento mapeia os controles técnicos e administrativos do MesaFlow para os frameworks de segurança mais exigidos pelo mercado Enterprise. Utilize esta matriz para preenchimento rápido de questionários de segurança (SIG, VSA, CAIQ).

---

## 1. SOC 2 - Trust Services Criteria (TSC)

| ID | Critério (CC) | Controle MesaFlow | Evidência / Documento |
| :--- | :--- | :--- | :--- |
| **CC1.3** | Management monitors internal control performance. | Auditoria contínua via scripts de validação e logs imutáveis. | `docs/enterprise/evidence_pack/ENTERPRISE_EVIDENCE_INDEX.md` |
| **CC2.1** | Information is protected from unauthorized access. | Autenticação JWT, RBAC e Row-Level Security (RLS). | `docs/technical/SECURITY_ARCHITECTURE.md` |
| **CC3.2** | Risk management program identifies risks. | Avaliação de Risco de Fornecedores (Vendor Risk). | `docs/enterprise/VENDOR_RISK_ASSESSMENT.md` |
| **CC5.2** | Logical access security software is used. | HSTS, CSP Strict, Rate Limiting (SlowAPI). | `app/main.py` (Middleware) |
| **CC6.1** | Logical access to system is restricted. | Controle de acesso baseado em função (RBAC) e MFA (Google Auth). | `docs/enterprise/evidence_pack/SECURITY_OVERVIEW.md` |
| **CC6.6** | Boundary protection devices are used. | WAF (via Vercel/Render) e Proteção contra DDoS. | `docs/enterprise/evidence_pack/ARCHITECTURE_OVERVIEW.md` |
| **CC7.1** | System components are monitored. | Observabilidade Fullstack (Sentry) e Health Checks. | `docs/tasks/TASK-GTM-02_OBSERVABILITY.md` |
| **CC8.1** | Change management process. | Protocolo de Mudança de Código e CI/CD Pipeline. | `docs/governance/CODE_CHANGE_PROTOCOL.md` |
| **A1.2** | Data availability and recovery. | Plano de Continuidade (BCP) e Backup (PITR). | `docs/enterprise/DR_BCP_PLAN.md` |
| **C1.1** | Data is identified and classified. | Política de Privacidade e RoPA. | `docs/legal/RoPA.md` |

---

## 2. ISO/IEC 27001:2013 (Annex A)

| ID | Controle | Implementação MesaFlow | Evidência |
| :--- | :--- | :--- | :--- |
| **A.5.1.1** | Policies for information security | Conjunto de Políticas de Segurança e Governança. | `docs/security/SECURITY_POLICY.md` |
| **A.8.2.1** | Classification of information | Classificação de dados no RoPA (Público, Interno, Confidencial). | `docs/legal/RoPA.md` |
| **A.9.2.1** | User registration and de-registration | Fluxo automatizado de onboarding/offboarding via Auth0/Google. | `app/routers/auth.py` |
| **A.9.4.1** | Information access restriction | Isolamento Multi-tenant via RLS (Database Enforcement). | `docs/technical/SECURITY_ARCHITECTURE.md` |
| **A.10.1.1** | Policy on the use of cryptographic controls | TLS 1.2+ em trânsito e AES-256 em repouso. | `docs/enterprise/evidence_pack/SECURITY_OVERVIEW.md` |
| **A.12.1.2** | Change management | Pipeline de CI/CD com testes automatizados. | `docs/DEVOPS.md` |
| **A.12.3.1** | Information backup | Backups automáticos e testes de restauração. | `docs/enterprise/DR_BCP_PLAN.md` |
| **A.12.4.1** | Event logging | Logs estruturados (JSON) e trilha de auditoria. | `app/core/logger.py` |
| **A.12.6.1** | Management of technical vulnerabilities | Pentest automatizado e gestão de dependências. | `scripts/security/automated_pentest.py` |
| **A.15.1.1** | Information security policy for supplier relationships | Política de Risco de Fornecedores. | `docs/enterprise/VENDOR_RISK_ASSESSMENT.md` |
| **A.16.1.1** | Responsibilities and procedures (Incident Mgmt) | Plano de Resposta a Incidentes. | `docs/enterprise/evidence_pack/INCIDENT_RESPONSE.md` |

---

## 3. LGPD / GDPR (Privacidade)

| Artigo | Requisito | Implementação | Documento |
| :--- | :--- | :--- | :--- |
| **Art. 6** | Princípios (Finalidade, Adequação) | Coleta mínima de dados e finalidade explícita. | `docs/legal/PRIVACY_POLICY.md` |
| **Art. 18** | Direitos do Titular | Canal de atendimento (DPO) e ferramentas de exportação. | `docs/legal/DATA_BREACH_NOTIFICATION.md` |
| **Art. 37** | Registro de Operações (RoPA) | Inventário de dados detalhado. | `docs/legal/RoPA.md` |
| **Art. 46** | Medidas de Segurança | Hardening, Criptografia e Controle de Acesso. | `docs/enterprise/evidence_pack/SECURITY_OVERVIEW.md` |

---
*Este mapeamento é uma ferramenta de referência e não substitui uma certificação formal emitida por auditor independente.*
