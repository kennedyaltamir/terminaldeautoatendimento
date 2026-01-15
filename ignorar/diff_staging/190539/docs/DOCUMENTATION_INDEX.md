# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-14 19:10:00

# 📚 Índice de Documentação MesaFlow
> Guia rápido de referência para todos os arquivos Markdown do projeto.

## 1. Raiz & Estratégia
- `README.md`: Visão geral do projeto, propósito e guia de início rápido.
- `MASTER_PROJECT_SPECIFICATION.md`: A "Bíblia" técnica do projeto, definindo arquitetura e regras imutáveis.
- `SECURITY.md`: Política de segurança e canal de denúncia de vulnerabilidades.
- `HANDOFF_MINIMAL.md`: Instruções mínimas para passar o projeto para outro desenvolvedor/IA.
- `MIGRATION_PLAN_DRAFT.md`: Rascunho inicial de estratégia de migração de dados.

## 2. Governança & Protocolos (`governance/`)
- `governance/README.md`: Explicação da estrutura de governança e status atual.
- `governance/DEFINITION_OF_DONE.md`: Checklist obrigatório para considerar uma tarefa concluída.
- `governance/DOMAIN_VALUES.md`: Lista de valores permitidos para Enums (Status, Roles, etc).
- `governance/ERROR_TAXONOMY.md`: Classificação padrão de erros do sistema.
- `governance/EXECUTION_ORDER_CYCLE_4.md`: Cronograma de execução do ciclo atual.
- `governance/HANDOVER_PACKAGE.md`: Modelo de pacote de transferência entre IAs.
- `governance/HOTFIX_L5_1.md`: Procedimento de emergência para correções em produção.
- `governance/HYPEROPTIMUS_MASTER_SPEC.md`: Especificação do motor de otimização cognitiva.
- `governance/IA_L5_TO_L6.md`: Plano de evolução da maturidade da IA.
- `governance/L6_AUTONOMOUS_EVOLUTION.md`: Manifesto da autonomia da IA nível 6.
- `governance/MATURITY_MODELS.md`: Definição dos níveis de maturidade (L1 a L6).
- `governance/OPTIMUS_v9_Architecture.md`: Arquitetura técnica do agente de automação Optimus.
- `governance/SOS_SYSTEM_STATE.md`: Protocolo de recuperação de desastres.
- `governance/TASK_CHECKLIST_TEMPLATE.md`: Modelo para criação de novas tarefas.

### Protocolos (`governance/protocols/`)
- `AI_ROLE_PROTOCOL.md`: Definição dos papéis da IA (Architect, Executor, etc).
- `AI_SCOPE_VIOLATION_PROTOCOL.md`: Regras para punir desvios de função da IA.
- `CODE_CHANGE_PROTOCOL.md`: Regras para alteração segura de código.
- `CONTEXT_GENERATION_PROTOCOL.md`: Como gerar o contexto para a IA.
- `CONTEXT_PRIORITY_PROTOCOL.md`: Hierarquia de documentos (TASKS.md > resto).
- `DOCUMENTATION_STANDARD_PROTOCOL.md`: Padrões de escrita e organização de docs.
- `ERROR_RESPONSE_MAPPING_PROTOCOL.md`: Como a IA deve reportar erros.
- `FAIL_FAST_PROTOCOL.md`: Regra de abortar execução ao primeiro sinal de erro.
- `FILE_OWNERSHIP_PROTOCOL.md`: Quem pode editar qual arquivo.
- `GOVERNANCE_CHANGE_PROTOCOL.md`: Como alterar as próprias regras de governança.
- `INDA_TASK_PROTOCOL.md`: O ciclo Inspection-Normalization-Decision-Action.
- `KERNEL_INDA_PROTOCOL.md`: Definição do Kernel como autoridade máxima.
- `MIHP_PROTOCOL.md`: Protocolo de transferência de contexto entre IAs.
- `ROLLBACK_PROTOCOL.md`: Procedimentos de reversão de mudanças.
- `SECURITY_BOUNDARY_PROTOCOL.md`: Limites de segurança que a IA não pode cruzar.
- `TASK_LIFECYCLE_PROTOCOL.md`: Estados de uma tarefa (Open -> Done).
- `UPDATE_EXECUTION_PROTOCOL.md`: Como o script `atualizar.py` deve funcionar.
- `VERIFICATION_PROTOCOL.md`: Regras para scripts de validação.

### Políticas (`governance/policies/`)
- `CHANGE_MANAGEMENT.md`: Política geral de gestão de mudanças.
- `DATA_PRIVACY.md`: Política de privacidade e LGPD.
- `deprecation_policy.md`: Como descontinuar funcionalidades.
- `enum_lifecycle.md`: Ciclo de vida de valores enumerados.
- `SECURITY.md`: Política de segurança específica (cópia/link da raiz).

### RFCs (`governance/rfc/`)
- `RFC-001.md`: Padrão do Context Bundle.
- `RFC-002.md`: Schema do Kernel Journal.
- `RFC-003.md`: Protocolo de Bootloader.
- `RFC-004.md`: Formato de Auto-Task.
- `RFC-005.md`: Protocolo de Snapshot do Kernel.
- `RFC-006.md`: Protocolo de Override de Governança.
- `RFC-007.md`: Definição de Fronteira de Segurança.
- `RFC-008.md`: Declaração de Baseline de Produção.
- `RFC-009.md`: Política de Hardening de Enums.
- `RFC-010.md`: Ciclo de Vida de Enums.
- `RFC-011.md`: Limites Operacionais de IA.
- `RFC-SCRIPT-ORGANIZATION.md`: Padrão de organização de scripts.

## 3. Evidências & Relatórios (`governance/evidence/`)
- `AUDIT_ENV_REPORT.md`: Resultado da auditoria de variáveis de ambiente.
- `BOOTSTRAP_SYNC_REPORT.md`: Log da sincronização inicial L6.
- `FINAL_L6_RESTRUCTURING_REPORT.md`: Relatório final da reestruturação de governança.
- `FIX_UNICODE_APPLIED.md`: Registro da correção de erro de encoding no Windows.
- `GAP_ANALYSIS_REPORT.md`: Análise de lacunas de scripts faltantes.
- `GOVERNANCE_METRICS.md`: Métricas atuais de qualidade e compliance.
- `GOVERNANCE_MIGRATION_L6_REPORT.md`: Log da migração para a estrutura L6.
- `INCIDENT_MOCK_DNS_RESOLUTION.md`: Registro de incidente de DNS em mock.
- `INCIDENT_UNICODE_WINDOWS.md`: Registro detalhado do erro de Unicode.
- `INSPECTION_REPORT_L6.md`: Relatório de inspeção de estado intermediário.
- `INSPECTION_REPORT_L6_FINAL.md`: Relatório final de inspeção.
- `MIGRATION_VERIFICATION_REPORT.md`: Validação da aplicação de migrações de banco.
- `PIPELINE_CANONICO.md`: Definição da ordem de execução dos scripts de validação.
- `REPORT_APP_01.md`: Validação de contexto ORM.
- `REPORT_APP_02.md`: Validação de idempotência.
- `REPORT_AUDITOR_SIMULATION.md`: Simulação de auditoria externa.
- `REPORT_BKP_01.md`: Diff estrutural de backups.
- `REPORT_DIAG_01.md`: Verificação de prontidão de dados.
- `REPORT_E2E_SUCCESS.md`: Confirmação de sucesso do teste ponta-a-ponta.
- `REPORT_ENUM_DRIFT.md`: Análise de divergência de Enums.
- `REPORT_ENUM_MIGRATION.md`: Log da migração de Enums.
- `REPORT_FINAL_STATUS.md`: Status final (parcial).
- `REPORT_FINAL_STATUS_v2.md`: Status final (aprovado).
- `REPORT_FINAL_STATUS_v3.md`: Status final (selado).
- `REPORT_FULL_COVERAGE.md`: Relatório de cobertura de rotas (Omniscience).
- `REPORT_GOLD_MASTER_V1.md`: Declaração de entrega Gold Master.
- `REPORT_GOVERNANCE_CHANGELOG.md`: Log de alterações nas regras de governança.
- `REPORT_GOV_01.md`: Validação de integridade de governança.
- `REPORT_GOV_01_XML_PRESENCE.md`: Auditoria de presença de XMLs.
- `REPORT_GOV_02.md`: Auditoria de headers de arquivos.
- `REPORT_GOV_03.md`: Validação de schema XML.
- `REPORT_GOV_04.md`: Relatório de drift do Registry.
- `REPORT_GOV_PROMPT_FIX.md`: Registro de correção de prompts.
- `REPORT_INF_01.md`: Healthcheck da API.
- `REPORT_INF_02.md`: Probe do Render.com.
- `REPORT_INF_03.md`: Check de latência Vercel.
- `REPORT_INF_04.md`: Probe do ambiente Expo.
- `REPORT_OBS_01.md`: Teste de ingestão Sentry.
- `REPORT_OBS_01_DIAG.md`: Diagnóstico de falha do Sentry.
- `REPORT_OMNISCIENCE.md`: Relatório geral de visibilidade do sistema.
- `REPORT_PHASE_1_CONCLUSION.md`: Conclusão da Fase 1.
- `REPORT_PHASE_2_CLOSURE.md`: Encerramento da Fase 2.
- `REPORT_PHASE_2_START.md`: Início da Fase 2.
- `REPORT_PHASE_3_READINESS.md`: Relatório de prontidão da Fase 3.
- `REPORT_QA_VISUAL_INSPECTION.md`: Relatório de inspeção visual manual.
- `REPORT_READINESS_SUMMARY.md`: Sumário executivo para investidores.
- `REPORT_SEC_01.md`: Auditoria de RLS (geral).
- `REPORT_SEC_01A.md`: Inventário de políticas RLS.
- `REPORT_SEC_01B.md`: Matriz de roles de banco.
- `REPORT_SEC_01C.md`: Teste de contexto efetivo.
- `REPORT_SEC_01D.md`: Prova passiva de RLS.
- `REPORT_SEC_01_FAILURE_ANALYSIS.md`: Análise de falha anterior do RLS.
- `REPORT_SEC_04.md`: Auditoria de variáveis de ambiente.
- `REPORT_SEC_05.md`: Auditoria de headers de segurança.
- `REPORT_SENTRY_SETUP.md`: Guia de configuração do Sentry.
- `REPORT_STRATEGIC_ALIGNMENT.md`: Alinhamento estratégico do projeto.
- `REPORT_SYSTEM_INTEGRITY.md`: Verificação de integridade de arquivos.
- `REPORT_SYSTEM_STABLE.md`: Declaração de estabilidade do sistema.
- `REPORT_UI_INTERACTIONS.md`: Auditoria de elementos interativos da UI.
- `REPORT_ZERO_CONFIG_GAPS.md`: Análise de lacunas de configuração zero.
- `RLS_CONTEXT_INSPECTION.md`: Inspeção detalhada do contexto RLS.
- `RLS_FAILURE_ANALYSIS.md`: Análise de falha de RLS.
- `RLS_FATAL_LEAK_REPORT.md`: Relatório de vazamento crítico de RLS.
- `RLS_GUC_REMEDIATION_LOG.md`: Log de remediação de configuração global do banco.
- `RLS_HARDENING_DIAGNOSTIC.md`: Diagnóstico de endurecimento do RLS.
- `RLS_MIGRATION_REPORT.md`: Log da migração de RLS.
- `RLS_POLICY_VERIFICATION.md`: Verificação de existência de políticas.
- `RLS_SUPERUSER_BYPASS_WARNING.md`: Alerta sobre bypass de superusuário.
- `RLS_VALIDATION_REPORT.md`: Relatório final de validação RLS.
- `SCHEMA_DISCOVERY_REPORT.md`: Mapeamento do schema atual do banco.
- `SECURITY_INCIDENT_RLS_LEAK.md`: Registro de incidente de segurança.
- `SECURITY_SEAL_L6.md`: Selo de segurança L6.
- `SQL_MIGRATION_REPORT.md`: Log de execução de migrações SQL.

## 4. Documentação Técnica (`docs/`)
- `docs/API.md`: Referência da API Backend.
- `docs/ARCHITECTURAL_DECISIONS.md`: Registro de decisões arquiteturais (ADRs).
- `docs/ARCHITECTURE.md`: Visão geral da arquitetura do sistema.
- `docs/AUDIT_REPORT_2026-01.md`: Relatório de auditoria geral de Janeiro.
- `docs/BACKLOG.md`: Lista de funcionalidades pendentes.
- `docs/CHANGELOG.md`: Histórico de mudanças do projeto.
- `docs/CONTRIBUTING.md`: Guia para contribuidores.
- `docs/DEEP_AUDIT_REPORT.md`: Relatório de auditoria profunda de código.
- `docs/DELIVERY_IMPROVEMENTS.md`: Plano de melhorias para o módulo de delivery.
- `docs/DEPLOY.md`: Guia de deploy.
- `docs/DEVOPS.md`: Práticas e ferramentas de DevOps.
- `docs/FRONTEND_STRUCTURE.md`: Estrutura de pastas do Frontend.
- `docs/GTM_CHECKLIST.md`: Checklist de Go-To-Market.
- `docs/GUIA_HARDWARE.md`: Guia de compatibilidade de impressoras e tablets.
- `docs/GUIA_STRIPE_ASSINATURAS.md`: Guia de integração com Stripe.
- `docs/IMPLEMENTATION_HISTORY.md`: Histórico de implementação.
- `docs/IMPLEMENTATION_LOG.md`: Log diário de implementação.
- `docs/IMPLEMENTATION_LOG_PHASE_7.md`: Log específico da Fase 7.
- `docs/INTEGRATION_HUB_GUIDE.md`: Guia de integrações externas.
- `docs/MANUAL_COZINHA.md`: Manual do usuário para a Cozinha (KDS).
- `docs/MANUAL_DELIVERY.md`: Manual do usuário para Delivery.
- `docs/MANUAL_FINANCEIRO.md`: Manual do usuário para Financeiro.
- `docs/MANUAL_GARCOM.md`: Manual do usuário para Garçons.
- `docs/MANUAL_GESTOR.md`: Manual do usuário para Gestores.
- `docs/MANUAL_PAGAMENTOS.md`: Manual de pagamentos.
- `docs/MASTER_CONTEXT.md`: Contexto mestre do projeto.
- `docs/MASTER_PROJECT_BIBLE.md`: Bíblia do projeto (visão completa).
- `docs/MESAFLOW_CONCEPT.md`: Conceito e visão do produto.
- `docs/OFFLINE_ARCHITECTURE_SPEC.md`: Especificação da arquitetura offline.
- `docs/PITCH.md`: Pitch de vendas do produto.
- `docs/PLAYBOOK_SUPORTE.md`: Playbook para equipe de suporte.
- `docs/PROJECT_OVERVIEW.md`: Visão geral do projeto.
- `docs/Projeto MesaFlow Corporate.md`: Especificação para versão corporativa.
- `docs/PRO_CHECKLIST.md`: Checklist para versão Pro.
- `docs/ROADMAP.md`: Roteiro de desenvolvimento futuro.
- `docs/ROUTE_TEST_REPORT.md`: Relatório de teste de rotas.
- `docs/SECURITY_AUDIT_REPORT.md`: Relatório de auditoria de segurança.
- `docs/SRE_MAINTENANCE_RUNBOOK.md`: Runbook de manutenção SRE.
- `docs/TASKS.md`: Lista mestre de tarefas (SSOT de execução).
- `docs/TECHNICAL_DEBT_REGISTER.md`: Registro de dívida técnica.
- `docs/TECH_DEBT.md`: Resumo de dívida técnica.

### ADRs (`docs/adr/`)
- `ADR-000_INDEX.md`: Índice de ADRs.
- `ADR-001_FASTAPI_BACKEND.md`: Decisão pelo FastAPI.
- `ADR-002_NEON_POSTGRESQL.md`: Decisão pelo Neon DB.
- `ADR-003_RENDER_RUNTIME.md`: Decisão pelo Render.
- `ADR-004_DUAL_HEALTH_ENDPOINT.md`: Decisão por endpoint duplo de saúde.
- `ADR-005_SECURITY_HARDENING_STRATEGY.md`: Estratégia de hardening de segurança.

### Mobile (`docs/mobile/`)
- `docs/mobile/README.md`: Visão geral do módulo Mobile.
- `docs/mobile/ENTERPRISE_STORE_CHECKLIST.md`: Checklist para lojas de app.
- `docs/mobile/PRINTER_HOMOLOGATION_GUIDE.md`: Guia de homologação de impressoras.
- `docs/mobile/TEST_PLAN_L6.md`: Plano de testes L6 para mobile.
- `docs/mobile/TEST_PLAN_MANUAL.md`: Roteiro de testes manuais mobile.
- `docs/mobile/architecture/*.md`: Documentos de arquitetura mobile.
- `docs/mobile/decisions/*.md`: Decisões técnicas mobile.
- `docs/mobile/reports/*.md`: Relatórios de execução mobile.
- `docs/mobile/setup/*.md`: Guias de setup mobile.
- `docs/mobile/tasks/*.md`: Logs de tasks mobile.
- `docs/mobile/testing/*.md`: Matrizes de teste mobile.

### Outros (`docs/`)
- `docs/architecture/domain-separation.md`: Separação de domínios.
- `docs/archive/`: Arquivos legados e históricos.
- `docs/audit/`: Relatórios de auditoria de código.
- `docs/commercial/`: Documentos comerciais e de vendas.
- `docs/cycles/`: Planejamento de ciclos de desenvolvimento.
- `docs/enterprise/`: Documentação específica para clientes Enterprise.
- `docs/frontend/`: Documentação específica do Frontend.
- `docs/implemented/`: Logs de funcionalidades implementadas.
- `docs/improvements/`: Propostas de melhoria.
- `docs/integration/`: Guias de integração.
- `docs/investors/`: Material para investidores.
- `docs/legal/`: Documentos legais (Termos, Privacidade).
- `docs/management/`: Documentos de gestão de projeto.
- `docs/manuals/`: Manuais de usuário e operação.
- `docs/manual_testing/`: Roteiros de teste manual.
- `docs/performance/`: Planejamento de capacidade.
- `docs/quality/`: Métricas de qualidade.
- `docs/releases/`: Notas de lançamento.
- `docs/reports/`: Relatórios gerais.
- `docs/security/`: Políticas de segurança.
- `docs/specs/`: Especificações funcionais.
- `docs/sre/`: Runbooks e planos de resposta a incidentes.
- `docs/strategy/`: Estratégia de produto.
- `docs/tasks/details/`: Detalhamento técnico de tasks específicas.
- `docs/team/`: Documentos de RH e contratação.
- `docs/technical/`: Documentação técnica profunda.
- `docs/troubleshooting/`: Guias de solução de problemas.
- `docs/trust/`: Documentação do Trust Center.

## 5. Frontend (`frontend/`)
- `frontend/README.md`: Instruções específicas do projeto Frontend.
- `frontend/test-results/`: Logs de erros de testes automatizados.

## 6. Comunicação (`comunication/`)
- `comunication/handoff_final.md`: Texto final de entrega.
- `comunication/handoff_log.md`: Log de transferência.
- `comunication/logs/`: Logs brutos de execução.
- `comunication/orders/`: Logs específicos de pedidos (debug).
- `comunication/prompts/`: Prompts utilizados para gerar código.
- `comunication/reports/`: Relatórios gerados por scripts (legado/backup).
