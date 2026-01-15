# 🚀 Guia Detalhado: Checklist de Produção (Hard Gate L6)

Este documento explica a racionalidade técnica por trás de cada item do `PRE_PRODUCTION_CHECKLIST.md`. O objetivo é garantir que o SRE ou o Arquiteto entenda *por que* um item é bloqueante.

## 1. Segurança (Cybersecurity)

### 1.1 RLS Ativo (Row-Level Security)
**Por que:** O MesaFlow é multi-tenant. Sem RLS, um erro de lógica no código (ex: esquecer um `.filter(company_id=...)`) permitiria que a Loja A visse os pedidos da Loja B.
**Como conferir:** Executar `scripts/validar/verify_TASK-SEC-01.py`. O banco deve retornar erro ou zero linhas ao tentar acessar IDs de outro tenant.

### 1.2 Secrets Audit
**Por que:** Chaves de teste (ex: `sk_test_...` do Stripe) em produção causam perda de receita real e falhas de conciliação.
**Como conferir:** O script `scripts/setup/audit_env.py` deve validar se as chaves iniciam com prefixos de produção (`sk_live`, `APP_USR`).

## 2. Infraestrutura (Reliability)

### 2.1 Healthcheck Multi-serviço
**Por que:** O sistema depende de uma "trindade": API, Banco e Redis. Se o Redis cair, o KDS para de atualizar em tempo real.
**Como conferir:** Acessar `/api/health`. O JSON deve reportar `status: healthy` para todos os componentes.

### 2.2 Latency Check (SLA)
**Por que:** Em um restaurante, 1 segundo de atraso na renderização do cardápio pode significar abandono de carrinho.
**Como conferir:** Rodar `scripts/validation/load_test_kds.py`. A latência P95 deve ser < 500ms.

## 3. Aplicação (Logic)

### 3.1 Omni-Check PASS
**Por que:** É a nossa vacina contra o retrabalho. Ele garante que a nova feature de "Cupom" não quebrou o "Cálculo de Imposto" que já funcionava.
**Como conferir:** Execução do script mestre de regressão.

### 3.2 Ledger Integrity
**Por que:** O Ledger é a prova jurídica de que o dinheiro entrou. Se a cadeia de hashes quebrar, não podemos garantir a auditoria financeira.
**Como conferir:** `scripts/tests/test_ledger_integrity.py`.
