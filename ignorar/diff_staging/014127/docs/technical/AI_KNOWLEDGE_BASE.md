# 🧠 MesaFlow AI Knowledge Base (Immune System)
**Status:** APPEND-ONLY / MANDATORY
**Versão:** 4.0 (Gold Master Edition)
**Objetivo:** Memória persistente para evitar repetição de erros técnicos e garantir a soberania do Kernel.

---

## 🏁 ESTADO ATUAL: GOLD MASTER SEALED (2026-01-15)
O sistema MesaFlow OS atingiu a maturidade L6. Todos os gates de segurança (RLS), infraestrutura (Healthcheck) e aplicação (Idempotência) foram validados via `master_readiness_check.py`.

---

## 🛠️ APRENDIZADOS CRÍTICOS & PADRÕES

### 2026-01-15 | KERNEL_STRICT_LEARNING (v8.3)
- **Regra:** O `atualizar.py` agora bloqueia execuções que não contenham a tag `<Knowledge_Accumulation>`.
- **Motivo:** Impedir a estagnação do conhecimento e garantir que cada correção seja documentada na base imunológica.
- **Perfil:** `AI_COGNITIVE_PROFILE.xml` elevado para v1.2 para reforçar esta obrigatoriedade.

### 2026-01-15 | FISCAL_SANDBOX_READY
- **Status:** Integração com Focus NFe validada via `smoke_test_focus_nfe.py`.
- **Bloqueio de Produção:** A emissão real exige obrigatoriamente um **Certificado Digital A1 (.pfx)** anexado ao painel da Focus. Sem isso, a API retorna erro 400 (Empresa não habilitada).
- **Configuração:** `FISCAL_PROVIDER=focus` e `FISCAL_ENV=sandbox` validados.

### 2026-01-15 | UI_PRICE_FORMATTING_FIX
- **Sintoma:** Preços aparecendo multiplicados por 100 (ex: R$ 2500,00 em vez de R$ 25,00).
- **Causa:** Exibição direta de valores inteiros (centavos) sem conversão.
- **Padrão:** Sempre utilizar a função `formatCurrency(valueInCents)` do `lib/utils.ts` para exibição e `parseCurrencyInput` para captura de dados.

### 2026-01-15 | DB_INTEGRITY_HANDLING
- **Sintoma:** Erro 500 ao excluir produtos com pedidos vinculados.
- **Causa:** `ForeignKeyViolation` no Postgres.
- **Correção:** O backend agora captura `IntegrityError` e retorna `409 Conflict` com mensagem instrutiva: "Desative o produto em vez de excluir".

### 2026-01-14 | INCIDENTE UNICODE WINDOWS
- **Aprendizado:** Terminais Windows crasham com emojis se não forçados para UTF-8.
- **Prevenção:** Injetado bloco de resiliência `io.TextIOWrapper` em todos os scripts críticos.

---

## 🗺️ INVENTÁRIO DE SOBERANIA
- **Constituição Cognitiva:** `governance/prompts/AI_COGNITIVE_PROFILE.xml`
- **Protocolo de Execução:** `governance/protocols/UPDATE_EXECUTION_PROTOCOL.md`
- **Dicionário de Telas:** `docs/technical/PAGE_DICTIONARY.md`
- **Validador Universal:** `scripts/validation/omni_check.py`

