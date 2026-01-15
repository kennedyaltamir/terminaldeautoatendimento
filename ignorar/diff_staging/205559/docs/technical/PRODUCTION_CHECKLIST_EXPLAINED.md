# 🚀 Guia Detalhado: Checklist de Produção (Hard Gate L6)

Este documento detalha os critérios técnicos para a selagem de produção. Um item marcado como "FAIL" no `registry.xml` bloqueia o deploy.

## 1. Segurança (Cybersecurity)

### 1.1 RLS (Row-Level Security) - [SEC-01]
- **O que é:** Filtro nativo do PostgreSQL que impede um Tenant de ver dados de outro.
- **Como validar:** O script `scripts/validar/verify_TASK-SEC-01.py` tenta realizar um "ataque lateral" (Tenant B tentando ler Order do Tenant A). O sucesso do teste é o retorno de zero registros.
- **Risco:** Vazamento de dados entre clientes concorrentes.

### 1.2 Secrets & Env Audit - [SEC-04]
- **O que é:** Varredura do arquivo `.env` em busca de chaves de teste ou valores vazios.
- **Como validar:** `scripts/setup/audit_env.py`. Ele verifica se `STRIPE_SECRET_KEY` começa com `sk_live` e se `MP_ACCESS_TOKEN` é válido.
- **Risco:** Perda de receita real por processamento em modo sandbox.

## 2. Infraestrutura (Reliability)

### 2.1 Healthcheck Multi-serviço - [INF-01]
- **O que é:** Verificação de conectividade da "Trindade Operacional" (API + DB + Redis).
- **Como validar:** `scripts/governance/inf_01_healthcheck.py`. Deve retornar `200 OK` com todos os serviços `up`.
- **Risco:** Sistema sobe, mas o KDS (WebSocket) não funciona por falta de Redis.

### 2.2 Latency & Stress - [INF-03]
- **O que é:** Garantia de que o sistema aguenta a carga de um evento real.
- **Como validar:** `scripts/validation/load_test_kds.py`. Simula 50 pedidos simultâneos. A latência média deve ser < 300ms.
- **Risco:** Travamento do sistema durante o horário de pico do restaurante.

## 3. Aplicação (Logic & Integrity)

### 3.1 Omni-Check (Anti-Retrabalho) - [SYS-01]
- **O que é:** Execução simultânea de todos os validadores do projeto.
- **Como validar:** `scripts/governance/run_doc_protocol.py`.
- **Risco:** Uma correção no Financeiro quebrar o Lançamento de Pedidos.

### 3.2 Ledger Hash Chain - [APP-02]
- **O que é:** Verificação da integridade da cadeia de blocos financeira.
- **Como validar:** `scripts/tests/test_ledger_integrity.py`. Recalcula todos os hashes do Ledger.
- **Risco:** Fraude interna ou corrupção de dados financeiros.
