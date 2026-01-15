
# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-13 12:35:00
# 🩺 Diagnóstico de Hardening RLS (Fase 2)

## 1. Identificação do Problema
O erro `UndefinedColumn: column "company_id" does not exist` revelou que a política de segurança global não pode ser "copy-paste" para todas as tabelas. Algumas tabelas no MesaFlow seguem uma hierarquia relacional onde o isolamento deve ser herdado.

## 2. Tabelas Identificadas sem `company_id`
- **products:** Vinculada via `category_id`.
- **order_items:** Vinculada via `order_id`.
- **option_groups:** Vinculada via `product_id`.

## 3. Estratégia de Correção (Isolamento Associativo)
Para estas tabelas, aplicamos políticas que utilizam subqueries para validar o dono do registro pai.
*Exemplo (Tabela products):*
`USING (category_id IN (SELECT id FROM categories WHERE company_id = {sessao}))`

## 4. Próximo Passo
Executar o novo script `apply_rls_hardening.py` v2. Ele detecta a necessidade de subqueries e aplica `FORCE ROW LEVEL SECURITY` para garantir que o isolamento funcione mesmo em conexões administrativas.

