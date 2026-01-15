
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 04:15:00
# 🛤️ Pipeline Canônico de Execução (MesaFlow Enterprise)

**Status:** DEFINITIVE
**Objetivo:** Roteiro de auditoria e validação para Go-Live e Due Diligence.

> **Nota:** Este documento define a *ordem lógica* e a *criticidade*. O estado real de execução reside em `registry.xml`.

## 1. GOVERNANÇA (Foundation)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **GOV-00** | `migrate_registry_enums_v10.py` | Normaliza status do registry. | **BLOCKING** | - |
| **GOV-01** | `gov_01_xml_presence_audit.py` | Audita existência de XMLs. | **BLOCKING** | GOV-00 |
| **GOV-02** | `gov_02_header_audit.py` | Garante headers de governança. | IMPORTANT | - |
| **GOV-03** | `gov_03_schema_validation.py` | Valida sintaxe XML. | **BLOCKING** | GOV-01 |
| **GOV-04** | `gov_04_registry_drift.py` | Audita drift Registry vs Pipeline. | IMPORTANT | - |

## 2. INFRAESTRUTURA (Connectivity)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **INF-01** | `inf_01_healthcheck.py` | Valida conectividade HTTP básica. | **BLOCKING** | GOV-03 |
| **INF-02** | `render_health_probe.py` | Valida endpoint Render. | OPTIONAL | INF-01 |
| **INF-03** | `vercel_latency_check.py` | Mede latência Frontend. | OPTIONAL | INF-02 |
| **INF-04** | `expo_runtime_probe.py` | Verifica ambiente Mobile. | OPTIONAL | - |

## 3. SEGURANÇA (Hardening)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **SEC-04** | `sec_04_env_audit.py` | Verifica segredos no .env. | **BLOCKING** | INF-01 |
| **SEC-01A** | `sec_01A_rls_policy_inventory.py` | Lista policies RLS ativas. | **BLOCKING** | SEC-04 |
| **SEC-01B** | `sec_01B_rls_role_matrix.py` | Valida permissões da role. | **BLOCKING** | SEC-01A |
| **SEC-01C** | `sec_01C_rls_effective_context.py` | Testa injeção de contexto. | **BLOCKING** | SEC-01B |
| **SEC-01D** | `sec_01D_rls_readonly_probe.py` | Tenta ler dados sem contexto. | **BLOCKING** | SEC-01C |
| **SEC-05** | `sec_05_boundary_audit.py` | Audita headers de segurança. | IMPORTANT | SEC-01D |

## 4. APLICAÇÃO (Logic & Integrity)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **APP-01** | `app_01_orm_context_sync.py` | Valida ORM Python context. | **BLOCKING** | SEC-01D |
| **APP-02** | `app_02_idempotency_validation.py` | Verifica trava de duplicidade. | IMPORTANT | APP-01 |
| **APP-03** | `app_03_transaction_check.py` | Verifica fronteiras transacionais. | IMPORTANT | APP-01 |
| **APP-04** | `app_04_error_handling.py` | Enforce tratamento de erros. | IMPORTANT | - |

## 5. DADOS (Consistency)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **DIAG-01** | `data_readiness_check.py` | Verifica dados mínimos (Seed). | **BLOCKING** | APP-01 |
| **DATA-02** | `data_integrity_scan.py` | Scan de integridade referencial. | IMPORTANT | DIAG-01 |
| **DATA-03** | `data_orphan_detection.py` | Detecção de órfãos. | OPTIONAL | DATA-02 |

## 6. OBSERVABILIDADE (Visibility)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **OBS-01** | `sentry_ingest_test.py` | Testa envio Sentry. | **BLOCKING** | SEC-04 |
| **OBS-02** | `obs_02_log_structure.py` | Valida estrutura de logs. | IMPORTANT | - |
| **OBS-03** | `obs_03_correlation_id.py` | Verifica correlation ID. | IMPORTANT | - |

## 7. BACKUP & RECOVERY (Resilience)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **BKP-01** | `backup_diff_audit.py` | Compara snapshots. | OPTIONAL | - |
| **BKP-02** | `bkp_02_snapshot_integrity.py` | Verifica integridade de zip. | IMPORTANT | - |

## 8. INVESTOR & GO-LIVE (Readiness)
| ID | Script | Função | Criticidade | Pré-requisito |
|:---|:---|:---|:---|:---|
| **INV-01** | `inv_01_zero_config.py` | Relatório Zero-Config. | **BLOCKING** | GOV-03, SEC-04, APP-01, DIAG-01, OBS-01 |
| **INV-02** | `inv_02_readiness_summary.py` | Sumário Executivo. | **BLOCKING** | INV-01 |
| **INV-03** | `inv_03_auditor_simulation.py` | Simulação de Auditoria. | **BLOCKING** | INV-02 |

---
*Aprovado para execução imediata.*

