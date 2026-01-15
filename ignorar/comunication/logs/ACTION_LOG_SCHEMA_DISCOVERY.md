
# LOG DE AÇÃO: DESCOBERTA DE SCHEMA
**Data:** 12/01/2026
**Executor:** Kernel-INDA
**Task:** SCHEMA-DISCOVERY

## 1. Ação Realizada
Criação do script `scripts/diagnostics/discover_schema.py` para mapear a verdade absoluta do banco de dados e eliminar suposições sobre tabelas inexistentes (ex: `customers`).

## 2. Detalhes Técnicos
- **Objetivo:** Listar tabelas, colunas, status de RLS e policies reais.
- **Método:** Introspecção via `pg_tables`, `information_schema` e `pg_policy`.
- **Segurança:** Read-only.
- **Output:** `comunication/reports/SCHEMA_DISCOVERY_REPORT.md`.

## 3. Status
- Script criado: ✅
- Registry atualizado: ✅
- Próximo passo: Execução manual e análise do relatório.

