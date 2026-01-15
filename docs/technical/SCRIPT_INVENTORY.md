
# 📜 SCRIPT INVENTORY — MesaFlow OS

**Versão:** 1.1 (Canonical Structure)  
**Data:** 2026-01-13  
**Autoridade:** Architect Kernel

Este inventário cataloga a localização física e funcional de todos os scripts operacionais do sistema, seguindo a estrutura de domínios isolados e a hierarquia suprema do SSOT.

---

## 🤖 automation/
*IA, bots, QA automático e auto-fix.*
- `auto_fix_on_fail.py`: Recuperação de estado em falhas de teste.
- `auto_fix_reporter_v4.py`: Gerador de relatórios de conformidade.
- `optimus_v9_1_neuro_evolution.py`: Cérebro de automação Playwright.
- `auto_calibrate_qa.py`: Calibração de coordenadas de interface.
- `gerar_contexto.py`: Coletor de contexto para IAs (HyperOptimus).

## 🔁 ci_cd/
*Gates, PR bots e integração contínua.*
- `ai_pr_guard.js`: Bot de veto para Pull Requests.
- `quality_gate_bot.js`: Verificador de métricas de qualidade em CI.

## 🏛️ governance/
*Auditorias, verificação e selagem de governança.*
- `gov_01_xml_presence_audit.py`: Auditoria de artefatos XML.
- `gov_02_header_audit.py`: Verificação de cabeçalhos de domínio.
- `gov_03_schema_validation.py`: Validação sintática de XMLs.
- `gov_04_registry_drift.py`: Detecção de divergência lógica vs física.
- `governance_dashboard.py`: Painel de métricas de governança.
- `seal_governance_v2.py`: Consolidador de estrutura de governança.
- `system_integrity_check.py`: Auditoria de caminhos críticos (SSOT).
- `verify_governance_structure.py`: Validador de conformidade de baseline.
- `governance_integrity_check.py`: Validador primário de XMLs.

## 🧹 maintenance/
*Higienização, diagnósticos e limpeza.*
- `analise_estrutural.py`: Mapeamento de diretórios raiz.
- `audit_script_inventory.py`: Sincronizador de inventário físico.
- `audit_structure.py`: Auditoria de arquivos críticos.
- `cleanup_context_noise.py`: Remoção de arquivos temporários de docs.
- `cleanup_final_sweep.py`: Higienização de arquivos soltos na raiz.
- `cleanup_scripts_noise.py`: Remoção de ruído em scripts de automação.
- `consolidate_reports.py`: Consolidação de relatórios forenses.
- `deep_audit_and_clean.py`: Auditoria industrial de integridade.
- `diagnose_api_errors.py`: Testador de endpoints críticos pós-fix.
- `find_heavy_files.py`: Scanner de arquivos gigantes (>50MB).
- `organize_optimus_docs.py`: Arquivista de documentação obsoleta.
- `organize_scripts.py`: Movimentador de scripts para filas de validação.
- `prepare_handoff.py`: Preparador de contexto para troca de IA.
- `standardize_scripts.py`: Padronizador de nomenclatura e diretórios.
- `sync_registry_mass.py`: Sincronizador massivo para o Registry.

## 🗄️ migrations/
*Banco de dados, Alembic e políticas RLS.*
- `fix_migration_imports.py`: Patch de imports em versões Alembic (Mantenibilidade).
- `apply_sql_migrations.py`: Aplicador de lotes SQL (Windows Safe).
- `apply_rls_migrations.py`: Aplicador de políticas RLS.
- `apply_rls_hardening.py`: Hardening L6 de isolamento associativo.
- `fix_enum_drift.py`: Conversor de ENUM para VARCHAR.
- `create_rls_policies.sql`: Definição de políticas SQL.
- `enable_rls_core_tables.sql`: Ativação de RLS.
- `fix_rls_policies.sql`: Correção de policies para UUID.
- `setup_secure_role.sql`: Provisionamento de Role restrita.

## 📈 observability/
*Healthchecks, probes e métricas de sistema.*
- `inf_01_healthcheck.py`: Healthcheck local API/DB.
- `render_health_probe.py`: Monitor de produção Render.com.
- `vercel_latency_check.py`: Teste de latência Frontend/Backend.
- `sentry_ingest_test.py`: Validador de telemetria Sentry.
- `data_readiness_check.py`: Verificador de prontidão de massa de dados.

## 🔐 security/
*RLS, enum drift, boundary e stress tests.*
- `sec_01A_rls_policy_inventory.py`: Inventário de proteção de tabelas.
- `sec_01B_rls_role_matrix.py`: Auditoria de privilégios de role.
- `sec_01C_rls_effective_context.py`: Teste de injeção de Session Variable.
- `sec_01D_rls_readonly_probe.py`: Prova passiva via EXPLAIN SQL.
- `sec_01_rls_integrity.py`: Teste de invasão lateral multi-tenant.
- `sec_05_boundary_audit.py`: Auditoria de headers HTTP de segurança.
- `verify_rls_public.py`: Validação de acesso anômino sob RLS.
- `stress_test_guards.py`: Teste de estresse em limites de IA.
- `provision_secure_role.py`: Provisionamento de conta `mesaflow_app`.

## ⚙️ setup/
*Bootstrap de ambiente, infra e segredos.*
- `env_execution_patch.py`: Patch para redirecionamento de DB local.
- `force_fix_env.py`: Injetor de chaves ausentes.
- `mock_production_env.py`: Gerador de .env blindado para auditoria.
- `patch_ifood_secret.py`: Patch específico para integração iFood.
- `setup_redis.py`: Orquestrador de Docker Redis.
- `seed.py`: Massa de dados inicial padrão.
- `seed_financial_data.py`: Cenário para auditoria financeira L7.
- `seed_ui_states.py`: Estados de UI para teste de estresse.

## ✅ validation/
*Verificações funcionais e prontidão para produção.*
- `master_readiness_check.py`: Gatekeeper final (MRC).
- `verify_TASK-SEC-01.py`: Validador canônico de RLS.
- `verify_TASK-AI-01.py`: Verificador de prontidão para IA.
- `verify_TASK-ESC-01.py`: Validador de segurança Webhook iFood.
- `otimizar.py`: Analisador de alinhamento e score de kernel.

## 🧪 verification/
*Testes de integridade profunda.*
- `hyperoptimus_tables_check.py`: Análise estática de render loops.

## 🚀 release/
*Rollback, launch e operações de release.*
- `auto_rollback.js`: Monitor de vitais com rollback EAS.
- `launch.bat`: Launcher de produção Windows.

## 🧩 tests_support/
*Scripts auxiliares e fixtures de testes.*
- `conftest.py`: Fixtures de banco em memória (SQLite).
- `e2e_system_flow.py`: Fluxo E2E simplificado.
- `e2e_system_flow_v2.py`: Fluxo E2E robusto.
- `test_circuit_breaker.py`: Simulador de falha controlada.
- `test_ledger_integrity.py`: Validador de hash de integridade L7.

## 📱 mobile/
*Scripts exclusivos da plataforma nativa.*
- `run_human_qa.py`: Orquestrador de testes Maestro/ADB.
- `verify_login_screen_l6.py`: Auditoria forense de renderização.
- `env_production_audit.py`: Scanner de segurança de variáveis mobile.
- `verify_eas_ready.py`: Check de ambiente de build cloud.
- `verify_production_ready.py`: Validador de arquivo LOCK.
- `verify_screen_resilience.py`: Check de resiliência visual.
- `verify_telemetry.py`: Validador de Sentry Mobile.
- `seal_production.py`: Gerador de selo de produção.
- `check_production_readiness.py`: Auditoria final de release.

## 🗑️ _archive/
*Backups de lógica, scripts obsoletos ou redundantes.*
- `fix_tables_route.py`
- `restore_evidence.py`
- `ops_01_cognitive_prune.py`
- `janitor_l7.py`
- `sanitize_repo.py`

---
*Assinado por: MesaFlow Kernel Executor. Alinhado ao SSOT.*

