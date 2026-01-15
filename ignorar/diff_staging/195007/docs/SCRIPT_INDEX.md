# 📜 Índice de Scripts & Automação
> **Gerado em:** 2026-01-14T19:48:47.336496
> **Total:** 142 scripts

## 📂 `Raiz`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [atualizar.py](../atualizar.py) | 🐍 | Implementa o RFC-002: Kernel Journal Schema |
| [dev.bat](../dev.bat) | 🐚 | 1. Verificar Python Virtualenv |
| [discover_schema.py](../discover_schema.py) | 🐍 | SELECT tablename |
| [gerartxt.py](../gerartxt.py) | 🐍 | Implementa o modo Git Delta: detecta arquivos modificados ou novos. |
| [run.py](../run.py) | 🐍 | Mata qualquer processo ocupando a porta especificada. |

## 📂 `alembic`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [env.py](../alembic/env.py) | 🐍 | 1. Adiciona o diretório atual ao Path |

## 📂 `alembic/versions`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [20260108_9999_rls_automagic.py](../alembic/versions/20260108_9999_rls_automagic.py) | 🐍 | rls automagic fix |
| [670e7aec4c77_fix_structural_integrity_and_add_ledger.py](../alembic/versions/670e7aec4c77_fix_structural_integrity_and_add_ledger.py) | 🐍 | fix_structural_integrity_and_add_ledger |

## 📂 `app`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [database.py](../app/database.py) | 🐍 | Define a variável de sessão do PostgreSQL para o Tenant atual. |
| [main.py](../app/main.py) | 🐍 | Sem descrição. |
| [models.py](../app/models.py) | 🐍 | ESTE ARQUIVO FOI MODULARIZADO PARA app/models/*.py |
| [schemas.py](../app/schemas.py) | 🐍 | ESTE ARQUIVO FOI MODULARIZADO PARA app/schemas/*.py |
| [websockets.py](../app/websockets.py) | 🐍 | Inicializa conexão com Redis e o worker de leitura do Pub/Sub. |

## 📂 `app/core`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [ai_guards.py](../app/core/ai_guards.py) | 🐍 | Decorator que impõe limites de tempo e memória para funções de IA. |
| [cache.py](../app/core/cache.py) | 🐍 | Decorator de cache inteligente que suporta funções síncronas e assíncronas. |
| [celery_app.py](../app/core/celery_app.py) | 🐍 | Configuração do Broker |
| [circuit_breaker.py](../app/core/circuit_breaker.py) | 🐍 | Sem descrição. |
| [docs.py](../app/core/docs.py) | 🐍 | Configurações de Metadados para a Documentação da API (Swagger/OpenAPI). |
| [limiter.py](../app/core/limiter.py) | 🐍 | Inicializa o limitador usando o IP do cliente como chave |
| [logger.py](../app/core/logger.py) | 🐍 | Formatador de logs para saída JSON estruturada. |
| [saas_limits.py](../app/core/saas_limits.py) | 🐍 | Verifica se a empresa pode criar mais produtos |
| [security.py](../app/core/security.py) | 🐍 | Gera um token de longa duração para renovação de sessão. |
| [utils.py](../app/core/utils.py) | 🐍 | Normaliza valores de Enum ou String para persistência segura no banco. |

## 📂 `app/models`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [auth.py](../app/models/auth.py) | 🐍 | Sem descrição. |
| [company.py](../app/models/company.py) | 🐍 | Sem descrição. |
| [core.py](../app/models/core.py) | 🐍 | 🛡️ SECURITY POLICY: ROW-LEVEL SECURITY (RLS) |
| [fintech.py](../app/models/fintech.py) | 🐍 | FINANCIAL LEDGER (L7) - HARDENED |
| [marketing.py](../app/models/marketing.py) | 🐍 | Sem descrição. |
| [menu.py](../app/models/menu.py) | 🐍 | Sem descrição. |
| [orders.py](../app/models/orders.py) | 🐍 | Sem descrição. |
| [public.py](../app/models/public.py) | 🐍 | Sem descrição. |
| [system.py](../app/models/system.py) | 🐍 | Sem descrição. |

## 📂 `app/routers`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [admin.py](../app/routers/admin.py) | 🐍 | Sem descrição. |
| [admin_ai.py](../app/routers/admin_ai.py) | 🐍 | Retorna a previsão de vendas para os próximos N dias. |
| [admin_audit.py](../app/routers/admin_audit.py) | 🐍 | Retorna os logs de auditoria do sistema para a empresa atual. |
| [admin_billing.py](../app/routers/admin_billing.py) | 🐍 | Sem descrição. |
| [admin_company.py](../app/routers/admin_company.py) | 🐍 | Retorna os dados da empresa com mascaramento de credenciais sensíveis. |
| [admin_delivery.py](../app/routers/admin_delivery.py) | 🐍 | Sem descrição. |
| [admin_employees.py](../app/routers/admin_employees.py) | 🐍 | Verifica se é um objeto Company (Dono) ou Employee com cargo de gerente |
| [admin_features.py](../app/routers/admin_features.py) | 🐍 | Retorna as flags da empresa atual. |
| [admin_financial.py](../app/routers/admin_financial.py) | 🐍 | Relatório de Gorjetas por Funcionário. |
| [admin_fiscal.py](../app/routers/admin_fiscal.py) | 🐍 | Sem descrição. |
| [admin_franchise.py](../app/routers/admin_franchise.py) | 🐍 | Sem descrição. |
| [admin_history.py](../app/routers/admin_history.py) | 🐍 | Sem descrição. |
| [admin_integrations.py](../app/routers/admin_integrations.py) | 🐍 | Sem descrição. |
| [admin_inventory.py](../app/routers/admin_inventory.py) | 🐍 | Retorna sugestões de compra agrupadas por fornecedor |
| [admin_logistics.py](../app/routers/admin_logistics.py) | 🐍 | Sem descrição. |
| [admin_marketing.py](../app/routers/admin_marketing.py) | 🐍 | Sem descrição. |
| [admin_menu.py](../app/routers/admin_menu.py) | 🐍 | Lista todos os produtos da empresa (Flat List). |
| [admin_metrics.py](../app/routers/admin_metrics.py) | 🐍 | Sem descrição. |
| [admin_payment.py](../app/routers/admin_payment.py) | 🐍 | Gera o link para o usuário conectar sua conta (ex: MP) |
| [admin_tables.py](../app/routers/admin_tables.py) | 🐍 | Gera um token numérico aleatório para acesso à mesa. |
| [auth.py](../app/routers/auth.py) | 🐍 | Revoga o token atual, adicionando seu JTI à blacklist no Redis. |
| [init.py](../app/routers/init.py) | 🐍 | Importa o router público do pacote (pasta), não do arquivo antigo |
| [payments.py](../app/routers/payments.py) | 🐍 | Simula o processamento de um pagamento online. |
| [upload.py](../app/routers/upload.py) | 🐍 | Faz upload de uma imagem com validação de segurança e persistência (S3 ou Local). |
| [webhooks.py](../app/routers/webhooks.py) | 🐍 | Webhook Hardened para baixa automática via Mercado Pago com Idempotência |
| [webhooks_ifood.py](../app/routers/webhooks_ifood.py) | 🐍 | SECURITY CONTRACT: IFOOD WEBHOOK (COMPLIANCE GRADE) |

## 📂 `app/routers/public`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [menu.py](../app/routers/public/menu.py) | 🐍 | Sem descrição. |
| [orders.py](../app/routers/public/orders.py) | 🐍 | Sem descrição. |
| [tables.py](../app/routers/public/tables.py) | 🐍 | Sem descrição. |

## 📂 `app/schemas`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [analytics.py](../app/schemas/analytics.py) | 🐍 | Sem descrição. |
| [auth.py](../app/schemas/auth.py) | 🐍 | Sem descrição. |
| [company.py](../app/schemas/company.py) | 🐍 | Sem descrição. |
| [core.py](../app/schemas/core.py) | 🐍 | Sem descrição. |
| [fintech.py](../app/schemas/fintech.py) | 🐍 | Sem descrição. |
| [inventory.py](../app/schemas/inventory.py) | 🐍 | --- SUPPLIER SCHEMAS --- |
| [marketing.py](../app/schemas/marketing.py) | 🐍 | Sem descrição. |
| [menu.py](../app/schemas/menu.py) | 🐍 | Sem descrição. |
| [orders.py](../app/schemas/orders.py) | 🐍 | --- TABLE SCHEMAS --- |
| [public.py](../app/schemas/public.py) | 🐍 | Sem descrição. |
| [staff.py](../app/schemas/staff.py) | 🐍 | Sem descrição. |
| [system.py](../app/schemas/system.py) | 🐍 | --- AUDIT SCHEMAS --- |

## 📂 `app/services`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [ai_prediction_service.py](../app/services/ai_prediction_service.py) | 🐍 | Retorna a previsão de vendas com proteção de recursos (RFC-011). |
| [audit_service.py](../app/services/audit_service.py) | 🐍 | Registra uma ação no log de auditoria. |
| [email_service.py](../app/services/email_service.py) | 🐍 | Envia e-mail de recuperação de senha via SMTP. |
| [feature_flag_service.py](../app/services/feature_flag_service.py) | 🐍 | Retorna todas as flags de uma empresa. |
| [fiscal_service.py](../app/services/fiscal_service.py) | 🐍 | Serviço de alto nível que orquestra a emissão fiscal. |
| [franchise_service.py](../app/services/franchise_service.py) | 🐍 | Sem descrição. |
| [ifood_service.py](../app/services/ifood_service.py) | 🐍 | Middleware de integração com iFood. |
| [importer_service.py](../app/services/importer_service.py) | 🐍 | Sem descrição. |
| [ledger_service.py](../app/services/ledger_service.py) | 🐍 | Motor de Integridade Financeira L7. |
| [logistics_service.py](../app/services/logistics_service.py) | 🐍 | Sem descrição. |
| [loyalty_service.py](../app/services/loyalty_service.py) | 🐍 | Calcula e credita o cashback na carteira do cliente após pagamento confirmado. |
| [metrics_service.py](../app/services/metrics_service.py) | 🐍 | KPIs |
| [order_service.py](../app/services/order_service.py) | 🐍 | Sem descrição. |
| [payment_service.py](../app/services/payment_service.py) | 🐍 | Calcula o valor da comissão (Split) com arredondamento seguro. |
| [promotion_service.py](../app/services/promotion_service.py) | 🐍 | Valida se um cupom é aplicável ao carrinho atual. |
| [purchase_service.py](../app/services/purchase_service.py) | 🐍 | <html> |
| [recommendation_service.py](../app/services/recommendation_service.py) | 🐍 | Sem descrição. |
| [reconciliation_service.py](../app/services/reconciliation_service.py) | 🐍 | Serviço de Conciliação Financeira L7. |
| [stock_service.py](../app/services/stock_service.py) | 🐍 | Baixa o estoque dos ingredientes de forma SÍNCRONA dentro da transação do pedido. |
| [storage_service.py](../app/services/storage_service.py) | 🐍 | Faz upload do arquivo e retorna a URL pública. |
| [stripe_service.py](../app/services/stripe_service.py) | 🐍 | Gera uma sessão de checkout do Stripe para upgrade de plano. |
| [token_service.py](../app/services/token_service.py) | 🐍 | Gerencia a revogação de tokens JWT utilizando Redis. |
| [webhook_dispatcher.py](../app/services/webhook_dispatcher.py) | 🐍 | Serviço responsável por orquestrar o envio de Webhooks. |
| [whatsapp_service.py](../app/services/whatsapp_service.py) | 🐍 | Serviço de integração com APIs de WhatsApp (Evolution API / Twilio). |

## 📂 `app/services/fiscal`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [factory.py](../app/services/fiscal/factory.py) | 🐍 | Fábrica que retorna a implementação correta do provedor fiscal. |
| [init.py](../app/services/fiscal/init.py) | 🐍 | Pacote de serviços fiscais |
| [interfaces.py](../app/services/fiscal/interfaces.py) | 🐍 | Interface abstrata para provedores de emissão fiscal. |

## 📂 `app/services/fiscal/providers`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [focus_nfe.py](../app/services/fiscal/providers/focus_nfe.py) | 🐍 | Integração com a API da Focus NFe v2. |
| [mock.py](../app/services/fiscal/providers/mock.py) | 🐍 | Simula a emissão fiscal para ambiente de desenvolvimento. |

## 📂 `app/services/payment`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [factory.py](../app/services/payment/factory.py) | 🐍 | Fábrica de Provedores de Pagamento. |
| [interfaces.py](../app/services/payment/interfaces.py) | 🐍 | Busca o histórico de transações no provedor para conciliação. |

## 📂 `app/services/payment/providers`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [mercadopago.py](../app/services/payment/providers/mercadopago.py) | 🐍 | Implementação do Provedor Mercado Pago com suporte a Auditoria L7. |

## 📂 `app/tasks`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [webhooks.py](../app/tasks/webhooks.py) | 🐍 | Task Celery para envio de Webhook com retries persistentes. |

## 📂 `comunication/scripts`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [app_01_orm_context_sync.py](../comunication/scripts/app_01_orm_context_sync.py) | 🐍 | APP-01: Verificação de propagação de contexto no ORM (v2 - Connection Aware). |
| [app_02_idempotency_validation.py](../comunication/scripts/app_02_idempotency_validation.py) | 🐍 | APP-02: Prova de Idempotência Financeira (v2 - Passive Validation). |
| [app_03_transaction_check.py](../comunication/scripts/app_03_transaction_check.py) | 🐍 | STUB RECOVERED |
| [app_04_error_handling.py](../comunication/scripts/app_04_error_handling.py) | 🐍 | STUB RECOVERED |
| [backup_diff_audit.py](../comunication/scripts/backup_diff_audit.py) | 🐍 | BKP-01: Backup Diff Audit (Refined). |
| [bkp_02_snapshot_integrity.py](../comunication/scripts/bkp_02_snapshot_integrity.py) | 🐍 | STUB RECOVERED |
| [data_integrity_scan.py](../comunication/scripts/data_integrity_scan.py) | 🐍 | STUB RECOVERED |
| [data_orphan_detection.py](../comunication/scripts/data_orphan_detection.py) | 🐍 | STUB RECOVERED |
| [data_readiness_check.py](../comunication/scripts/data_readiness_check.py) | 🐍 | DIAG-01: Data Readiness Check. |
| [expo_runtime_probe.py](../comunication/scripts/expo_runtime_probe.py) | 🐍 | INF-04: Expo Runtime Probe. |
| [gov_01_xml_presence_audit.py](../comunication/scripts/gov_01_xml_presence_audit.py) | 🐍 | 🏛️ GOVERNANCE XML PRESENCE AUDIT (GOV-01) |
| [gov_02_header_audit.py](../comunication/scripts/gov_02_header_audit.py) | 🐍 | GOV-02: Mandatory Header Audit (v2.1 - High Performance). |
| [gov_03_schema_validation.py](../comunication/scripts/gov_03_schema_validation.py) | 🐍 | 🏛️ GOVERNANCE XML SCHEMA VALIDATION (GOV-03) |
| [gov_04_registry_drift.py](../comunication/scripts/gov_04_registry_drift.py) | 🐍 | Busca o script recursivamente dentro da pasta /scripts. |
| [governance_integrity_check.py](../comunication/scripts/governance_integrity_check.py) | 🐍 | GOV-01: Governance Integrity Check. |
| [inf_01_healthcheck.py](../comunication/scripts/inf_01_healthcheck.py) | 🐍 | 📊 HEALTHCHECK VALIDATOR (INF-01) - Governance v4 Aligned |
| [inv_01_zero_config.py](../comunication/scripts/inv_01_zero_config.py) | 🐍 | 🔌 ZERO-CONFIG GAP ANALYZER (INV-01) |
| [inv_02_readiness_summary.py](../comunication/scripts/inv_02_readiness_summary.py) | 🐍 | 📊 EXECUTIVE READINESS SUMMARY (INV-02) - ROBUST |
| [inv_03_auditor_simulation.py](../comunication/scripts/inv_03_auditor_simulation.py) | 🐍 | 🕵️ EXTERNAL AUDITOR SIMULATION (INV-03) - ROBUST |
| [migrate_registry_enums_v10.py](../comunication/scripts/migrate_registry_enums_v10.py) | 🐍 | STUB RECOVERED |
| [obs_02_log_structure.py](../comunication/scripts/obs_02_log_structure.py) | 🐍 | STUB RECOVERED |
| [obs_03_correlation_id.py](../comunication/scripts/obs_03_correlation_id.py) | 🐍 | STUB RECOVERED |
| [ops_01_cognitive_prune.py](../comunication/scripts/ops_01_cognitive_prune.py) | 🐍 | ID: OPS-01 |
| [render_health_probe.py](../comunication/scripts/render_health_probe.py) | 🐍 | INF-02: Render Health Probe. |
| [sec_01A_rls_policy_inventory.py](../comunication/scripts/sec_01A_rls_policy_inventory.py) | 🐍 | SEC-01A: Auditoria de Existência e Força de Políticas RLS. |
| [sec_01B_rls_role_matrix.py](../comunication/scripts/sec_01B_rls_role_matrix.py) | 🐍 | SEC-01B: Auditoria de Roles e Privilégios. |
| [sec_01C_rls_effective_context.py](../comunication/scripts/sec_01C_rls_effective_context.py) | 🐍 | SEC-01C: Validação de Propagação de Contexto. |
| [sec_01D_rls_readonly_probe.py](../comunication/scripts/sec_01D_rls_readonly_probe.py) | 🐍 | SEC-01D: Prova de Conceito de Filtro RLS via EXPLAIN. |
| [sec_01_rls_integrity.py](../comunication/scripts/sec_01_rls_integrity.py) | 🐍 | SEC-01: Validador de RLS Hardened v2. |
| [sec_04_env_audit.py](../comunication/scripts/sec_04_env_audit.py) | 🐍 | SEC-04: Secrets & Env Audit. |
| [sec_05_boundary_audit.py](../comunication/scripts/sec_05_boundary_audit.py) | 🐍 | 🛡️ SECURITY BOUNDARY AUDIT (SEC-05) |
| [sentry_ingest_test.py](../comunication/scripts/sentry_ingest_test.py) | 🐍 | OBS-01: Sentry Ingest Test. |
| [vercel_latency_check.py](../comunication/scripts/vercel_latency_check.py) | 🐍 | INF-03: Vercel to Backend Latency Check. |

## 📂 `comunication/scripts/maintenance`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [migrate_registry_enums_v10.py](../comunication/scripts/maintenance/migrate_registry_enums_v10.py) | 🐍 | 📉 REGISTRY ENUM MIGRATOR V10.2 (SILENT) |

## 📂 `frontend`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [next-env.d.ts](../frontend/next-env.d.ts) | 🐚 | <reference types="next" /> |
| [next.config.ts](../frontend/next.config.ts) | 🐚 | Habilita rotas tipadas (Nativo no Next.js 16) |
| [playwright.config.ts](../frontend/playwright.config.ts) | 🐚 | Aumentado para 2 minutos (Global) para suportar compilação lenta no Windows |
| [postcss.config.js](../frontend/postcss.config.js) | 🐚 | Sem descrição. |
| [sentry.client.config.ts](../frontend/sentry.client.config.ts) | 🐚 | Ajuste de amostragem para produção |
| [sentry.edge.config.ts](../frontend/sentry.edge.config.ts) | 🐚 | Amostragem para Edge Functions |
| [sentry.server.config.ts](../frontend/sentry.server.config.ts) | 🐚 | Amostragem de performance no servidor |

## 📂 `frontend/public`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [sw.js](../frontend/public/sw.js) | 🐚 | Sem descrição. |
| [workbox-f1770938.js](../frontend/public/workbox-f1770938.js) | 🐚 | Sem descrição. |

## 📂 `frontend/src`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [middleware.ts](../frontend/src/middleware.ts) | 🐚 | 1. Obter o Hostname (ex: pedidos.loja.com ou localhost:3000) |

## 📂 `scripts/automation`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [auto_fix_reporter_v4.py](../scripts/automation/auto_fix_reporter_v4.py) | 🐍 | 🛠️ AUTO FIX REPORTER v4 (Compliance Edition) |
| [optimus_v9_1_neuro_evolution.py](../scripts/automation/optimus_v9_1_neuro_evolution.py) | 🐍 | Lógica de Login Robusta e Explícita. |
| [run_human_qa.py](../scripts/automation/run_human_qa.py) | 🐍 | Captura screenshot e dump XML para diagnóstico. |
| [ui_sanity_check.py](../scripts/automation/ui_sanity_check.py) | 🐍 | 1. Verificar se existem propriedades 'undefined' nos estilos |
| [ui_sweep_mobile.py](../scripts/automation/ui_sweep_mobile.py) | 🐍 | Activity padrão para Expo Managed Workflow |
| [verify_login_screen_l6.py](../scripts/automation/verify_login_screen_l6.py) | 🐍 | Sem descrição. |

## 📂 `scripts/collector`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [gerar_contexto.py](../scripts/collector/gerar_contexto.py) | 🐍 | Retorna o SHA-256 de um arquivo. |

## 📂 `scripts/documentation`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [generate_api_ref.py](../scripts/documentation/generate_api_ref.py) | 🐍 | Adiciona raiz ao path |
| [generate_full_index.py](../scripts/documentation/generate_full_index.py) | 🐍 | Lê o arquivo e tenta extrair um Título e uma Descrição. |
| [generate_script_index.py](../scripts/documentation/generate_script_index.py) | 🐍 | Extrai descrição de Docstrings ou comentários. |

## 📂 `scripts/github`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [ai_pr_guard.js](../scripts/github/ai_pr_guard.js) | 🐚 | Limites de Qualidade L5 |
| [quality_gate_bot.js](../scripts/github/quality_gate_bot.js) | 🐚 | Configuração L5 |

## 📂 `scripts/governance`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [gov_04_registry_drift.py](../scripts/governance/gov_04_registry_drift.py) | 🐍 | Busca o script recursivamente dentro da pasta /scripts. |
| [run_doc_protocol.py](../scripts/governance/run_doc_protocol.py) | 🐍 | 📚 MESAFLOW DOCUMENTATION PROTOCOL ORCHESTRATOR |
| [system_integrity_check.py](../scripts/governance/system_integrity_check.py) | 🐍 | Fix para encoding no Windows (ORD-001) |

## 📂 `scripts/l6`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [auto_calibrate_qa.py](../scripts/l6/auto_calibrate_qa.py) | 🐍 | Busca as coordenadas de um elemento pelo texto no dump atual da tela. |
| [auto_fix_on_fail.py](../scripts/l6/auto_fix_on_fail.py) | 🐍 | Wrapper para tentar uma ação, executar auto-fix se falhar, e tentar novamente. |

## 📂 `scripts/maintenance`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [analise_estrutural.py](../scripts/maintenance/analise_estrutural.py) | 🐍 | Configuração de pastas para ignorar (reduz ruído) |
| [audit_mobile_l4.py](../scripts/maintenance/audit_mobile_l4.py) | 🐍 | Sem descrição. |
| [audit_mobile_production.py](../scripts/maintenance/audit_mobile_production.py) | 🐍 | Sem descrição. |
| [audit_script_inventory.py](../scripts/maintenance/audit_script_inventory.py) | 🐍 | 📜 SCRIPT INVENTORY AUDITOR (Omniscience Phase C) |
| [audit_structure.py](../scripts/maintenance/audit_structure.py) | 🐍 | CONFIGURAÇÃO DE AUDITORIA ESTRUTURAL |
| [check_production_readiness.py](../scripts/maintenance/check_production_readiness.py) | 🐍 | Sem descrição. |
| [cleanup_context_noise.py](../scripts/maintenance/cleanup_context_noise.py) | 🐍 | Configuração |
| [cleanup_final_sweep.py](../scripts/maintenance/cleanup_final_sweep.py) | 🐍 | CONFIGURAÇÃO DE LIMPEZA DA RAIZ |
| [cleanup_scripts_noise.py](../scripts/maintenance/cleanup_scripts_noise.py) | 🐍 | CONFIGURAÇÃO DE LIMPEZA DE SCRIPTS (Optimus v9 Context) |
| [collect_markdowns.py](../scripts/maintenance/collect_markdowns.py) | 🐍 | 📚 MARKDOWN COLLECTOR (Safe Mode) |
| [consolidate_reports.py](../scripts/maintenance/consolidate_reports.py) | 🐍 | Sem descrição. |
| [deep_audit_and_clean.py](../scripts/maintenance/deep_audit_and_clean.py) | 🐍 | 🧹 DEEP AUDIT & CLEANER v1.0 (Industrial Grade) |
| [diagnose_api_errors.py](../scripts/maintenance/diagnose_api_errors.py) | 🐍 | Configuração |
| [diagnose_tables_data.py](../scripts/maintenance/diagnose_tables_data.py) | 🐍 | Adiciona a raiz ao path |
| [doc_cleanup_l7.py](../scripts/maintenance/doc_cleanup_l7.py) | 🐍 | 🧹 DOCUMENTATION JANITOR L7 |
| [env_production_audit.py](../scripts/maintenance/env_production_audit.py) | 🐍 | Configuração |
| [find_heavy_files.py](../scripts/maintenance/find_heavy_files.py) | 🐍 | Sem descrição. |
| [fix_broken_links.py](../scripts/maintenance/fix_broken_links.py) | 🐍 | 🔗 BROKEN LINK FIXER (Auto-Correction) |
| [fix_drift_evidence.py](../scripts/maintenance/fix_drift_evidence.py) | 🐍 | Procura o arquivo recursivamente na pasta ignorar. |
| [fix_enum_drift.py](../scripts/maintenance/fix_enum_drift.py) | 🐍 | ALTER TABLE companies |
| [fix_migration_imports.py](../scripts/maintenance/fix_migration_imports.py) | 🐍 | Insere o import logo após os imports padrão do alembic |
| [fix_registry_drift_comprehensive.py](../scripts/maintenance/fix_registry_drift_comprehensive.py) | 🐍 | Procura o arquivo recursivamente na pasta ignorar. |
| [fix_tables_route.py](../scripts/maintenance/fix_tables_route.py) | 🐍 | Adiciona o diretório raiz ao path para importar app.database |
| [governance_dashboard.py](../scripts/maintenance/governance_dashboard.py) | 🐍 | Lê o último score real do otimizar.py. |
| [import_sanity_check.py](../scripts/maintenance/import_sanity_check.py) | 🐍 | Adiciona a raiz ao path |
| [janitor_governance.py](../scripts/maintenance/janitor_governance.py) | 🐍 | 🧹 JANITOR GOVERNANCE (NEUTRALIZED) |
| [janitor_l7.py](../scripts/maintenance/janitor_l7.py) | 🐍 | 🎯 ALVOS DE ELIMINAÇÃO (RUÍDO COGNITIVO) |
| [kernel_reset.py](../scripts/maintenance/kernel_reset.py) | 🐍 | 🧹 KERNEL JOURNAL ROTATION & RESET |
| [migrate_governance_structure.py](../scripts/maintenance/migrate_governance_structure.py) | 🐍 | 🏗️ GOVERNANCE MIGRATOR v4.0 |
| [mobile_build_audit.py](../scripts/maintenance/mobile_build_audit.py) | 🐍 | Configuração |
| [mobile_hard_reset.py](../scripts/maintenance/mobile_hard_reset.py) | 🐍 | 1. Remover pastas de build nativo que causam o conflito 'Bare Workflow' |
| [mobile_runtime_sanity.py](../scripts/maintenance/mobile_runtime_sanity.py) | 🐍 | Configuração |
| [mobile_runtime_sanity.ts](../scripts/maintenance/mobile_runtime_sanity.ts) | 🐚 | Sem descrição. |
| [open_qa_tabs.py](../scripts/maintenance/open_qa_tabs.py) | 🐍 | Configuração |
| [organize_governance.py](../scripts/maintenance/organize_governance.py) | 🐍 | Sem descrição. |
| [organize_optimus_docs.py](../scripts/maintenance/organize_optimus_docs.py) | 🐍 | Configuração |
| [organize_scripts.py](../scripts/maintenance/organize_scripts.py) | 🐍 | 🧹 SCRIPT ORGANIZER (Governance Enforcement) |
| [prepare_handoff.py](../scripts/maintenance/prepare_handoff.py) | 🐍 | Sem descrição. |
| [production_absolute_audit.py](../scripts/maintenance/production_absolute_audit.py) | 🐍 | Sem descrição. |
| [production_lock_mobile.py](../scripts/maintenance/production_lock_mobile.py) | 🐍 | Sem descrição. |
| [provision_secure_role.py](../scripts/maintenance/provision_secure_role.py) | 🐍 | DO $$ |
| [restore_evidence.py](../scripts/maintenance/restore_evidence.py) | 🐍 | 🚑 EVIDENCE RESTORATION TOOL |
| [run_ui_sweep.py](../scripts/maintenance/run_ui_sweep.py) | 🐍 | Ativa ou desativa o modo UI Sweep no App.tsx |
| [sanitize_repo.py](../scripts/maintenance/sanitize_repo.py) | 🐍 | Configuração de Preservação (O que NÃO mover) |
| [seal_governance_v2.py](../scripts/maintenance/seal_governance_v2.py) | 🐍 | 1. Organizar Prompts/Perfis |
| [seal_production.py](../scripts/maintenance/seal_production.py) | 🐍 | Sem descrição. |
| [seed_financial_data.py](../scripts/maintenance/seed_financial_data.py) | 🐍 | Adiciona a raiz ao path para importações do app |
| [seed_ui_states.py](../scripts/maintenance/seed_ui_states.py) | 🐍 | Adiciona o diretório raiz ao path |
| [standardize_scripts.py](../scripts/maintenance/standardize_scripts.py) | 🐍 | CONFIGURAÇÃO DA PADRONIZAÇÃO |
| [sync_registry_mass.py](../scripts/maintenance/sync_registry_mass.py) | 🐍 | 🔄 MASS REGISTRY SYNCHRONIZER (ROBUST) |
| [system_integrity_check.py](../scripts/maintenance/system_integrity_check.py) | 🐍 | Windows Resilience: Force UTF-8 Output |
| [verify_eas_ready.py](../scripts/maintenance/verify_eas_ready.py) | 🐍 | shell=True necessário no Windows para resolver PATH do npm/npx |
| [verify_mobile_syntax.py](../scripts/maintenance/verify_mobile_syntax.py) | 🐍 | Sem descrição. |
| [verify_production_ready.py](../scripts/maintenance/verify_production_ready.py) | 🐍 | Sem descrição. |
| [verify_screen_resilience.py](../scripts/maintenance/verify_screen_resilience.py) | 🐍 | Sem descrição. |
| [verify_telemetry.py](../scripts/maintenance/verify_telemetry.py) | 🐍 | 1. Verificar Dependência |

## 📂 `scripts/migrations`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [apply_rls_hardening.py](../scripts/migrations/apply_rls_hardening.py) | 🐍 | Fallback decoder for Windows Postgres errors. |

## 📂 `scripts/production`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [launch.bat](../scripts/production/launch.bat) | 🐚 | 1. Verificações Finais |

## 📂 `scripts/release`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [auto_rollback.js](../scripts/release/auto_rollback.js) | 🐚 | Mock de dados do Sentry (Em produção, chamaria a API do Sentry) |

## 📂 `scripts/scripts/setup`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [refresh_mobile_app.ps1](../scripts/scripts/setup/refresh_mobile_app.ps1) | 🐚 | Script de Atualização Rápida do App no Emulador |

## 📂 `scripts/security`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [audit_enum_drift.py](../scripts/security/audit_enum_drift.py) | 🐍 | Adiciona a raiz ao path para importações do app |
| [audit_enum_usage_v3.py](../scripts/security/audit_enum_usage_v3.py) | 🐍 | Configuração |
| [stress_test_guards.py](../scripts/security/stress_test_guards.py) | 🐍 | Tenta acessar pedido que não pertence ao Tenant A |
| [verify_rls_public.py](../scripts/security/verify_rls_public.py) | 🐍 | Adiciona a raiz ao path |

## 📂 `scripts/setup`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [activate_gold_master.py](../scripts/setup/activate_gold_master.py) | 🐍 | 🏆 MESAFLOW GOLD MASTER ACTIVATOR |
| [audit_env.py](../scripts/setup/audit_env.py) | 🐍 | 🛡️ PRODUCTION ENV AUDITOR v3.7 (Environment Aware) |
| [env_execution_patch.py](../scripts/setup/env_execution_patch.py) | 🐍 | 🌉 ENV EXECUTION PATCH v1.2 — Password Aware |
| [fix_local_redis.py](../scripts/setup/fix_local_redis.py) | 🐍 | Tenta importar redis, se não tiver, avisa |
| [force_connect_redis.py](../scripts/setup/force_connect_redis.py) | 🐍 | Tenta importar redis |
| [force_fix_env.py](../scripts/setup/force_fix_env.py) | 🐍 | Lê o conteúdo atual |
| [force_redis_ip.py](../scripts/setup/force_redis_ip.py) | 🐍 | Tenta importar redis |
| [mock_production_env.py](../scripts/setup/mock_production_env.py) | 🐍 | # MESAFLOW PRODUCTION MOCK (AUDIT COMPLIANT) |
| [patch_ifood_secret.py](../scripts/setup/patch_ifood_secret.py) | 🐍 | Sem descrição. |
| [restore_dev_env.py](../scripts/setup/restore_dev_env.py) | 🐍 | ENVIRONMENT=development |
| [setup_redis.py](../scripts/setup/setup_redis.py) | 🐍 | Tenta executar o comando. No Windows, shell=True é necessário para comandos do sistema. |
| [smart_redis_setup.py](../scripts/setup/smart_redis_setup.py) | 🐍 | Tenta importar redis |

## 📂 `scripts/tests`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [conftest.py](../scripts/tests/conftest.py) | 🐍 | Cria uma nova sessão de banco de dados para cada teste. |
| [e2e_system_flow.py](../scripts/tests/e2e_system_flow.py) | 🐍 | 🧪 E2E SYSTEM FLOW TEST (Omniscience Phase D) |
| [e2e_system_flow_v2.py](../scripts/tests/e2e_system_flow_v2.py) | 🐍 | 🧪 E2E SYSTEM FLOW TEST v2.1 (Dynamic ID Fix) |
| [test_circuit_breaker.py](../scripts/tests/test_circuit_breaker.py) | 🐍 | Sem descrição. |
| [test_ledger_integrity.py](../scripts/tests/test_ledger_integrity.py) | 🐍 | Sem descrição. |

## 📂 `scripts/validar`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [apply_rls_migrations.py](../scripts/validar/apply_rls_migrations.py) | 🐍 | Aplica as políticas de Row-Level Security (RLS) em massa. |
| [apply_sql_migrations.py](../scripts/validar/apply_sql_migrations.py) | 🐍 | 🛡️ SQL MIGRATION APPLIER (Windows Safe) |
| [discover_schema.py](../scripts/validar/discover_schema.py) | 🐍 | Sem descrição. |
| [enterprise_ui_explorer_v5_1.py](../scripts/validar/enterprise_ui_explorer_v5_1.py) | 🐍 | () => { |
| [inspect_rls_context.py](../scripts/validar/inspect_rls_context.py) | 🐍 | 🕵️ RLS CONTEXT INSPECTOR (Windows Safe) |
| [master_readiness_check.py](../scripts/validar/master_readiness_check.py) | 🐍 | 🚦 MASTER READINESS CHECK (MRC) v3.4 — Windows Unicode Resilience |
| [mobile_production_gate.py](../scripts/validar/mobile_production_gate.py) | 🐍 | 1. Check Hardcoded IPs |
| [otimizar.py](../scripts/validar/otimizar.py) | 🐍 | Sem descrição. |
| [reconcile_payments.py](../scripts/validar/reconcile_payments.py) | 🐍 | Adiciona a raiz ao path para importações do app |
| [seed.py](../scripts/validar/seed.py) | 🐍 | Sem descrição. |
| [verify_TASK-SEC-01.py](../scripts/validar/verify_TASK-SEC-01.py) | 🐍 | Sem descrição. |
| [verify_governance_structure.py](../scripts/validar/verify_governance_structure.py) | 🐍 | Gera visualizacao da arvore de diretorios em ASCII. |
| [verify_migrations_applied.py](../scripts/validar/verify_migrations_applied.py) | 🐍 | 🛡️ MIGRATION VERIFIER (Windows Safe) |
| [verify_rls_policies_exist.py](../scripts/validar/verify_rls_policies_exist.py) | 🐍 | 🛡️ RLS POLICY VERIFIER (Windows Safe) |

## 📂 `scripts/validation`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [load_test_kds.py](../scripts/validation/load_test_kds.py) | 🐍 | Cria um pedido único simulando um cliente. |
| [master_readiness_check.py](../scripts/validation/master_readiness_check.py) | 🐍 | 🚦 MASTER READINESS CHECK (MRC) v3.2 — Gold Master Edition |
| [otimizar.py](../scripts/validation/otimizar.py) | 🐍 | Sem descrição. |
| [system_omniscience_probe.py](../scripts/validation/system_omniscience_probe.py) | 🐍 | Fix para Windows Unicode |
| [ui_interaction_audit.py](../scripts/validation/ui_interaction_audit.py) | 🐍 | Fix para Windows Unicode |
| [verify_TASK-AI-01.py](../scripts/validation/verify_TASK-AI-01.py) | 🐍 | Adiciona a raiz ao path |
| [verify_TASK-ESC-01.py](../scripts/validation/verify_TASK-ESC-01.py) | 🐍 | Sem descrição. |
| [verify_TASK-SEC-01.py](../scripts/validation/verify_TASK-SEC-01.py) | 🐍 | Sem descrição. |

## 📂 `scripts/verification`
| Script | Tipo | Descrição |
| :--- | :---: | :--- |
| [hyperoptimus_tables_check.py](../scripts/verification/hyperoptimus_tables_check.py) | 🐍 | HYPEROPTIMUS VERIFICATION SCRIPT |
