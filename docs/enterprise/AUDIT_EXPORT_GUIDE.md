# 🕵️ Guia de Exportação de Logs de Auditoria (SIEM Integration)

**Público Alvo:** Equipes de Segurança (SecOps), Auditores e Administradores.
**Objetivo:** Extrair logs de auditoria do MesaFlow para análise externa ou arquivamento legal.

---

## 1. Visão Geral
O MesaFlow fornece um endpoint seguro para exportação em lote de logs de auditoria. Os dados são fornecidos em formato **CSV (Comma Separated Values)**, compatível com a maioria das ferramentas de SIEM (Splunk, ELK, Datadog) e planilhas (Excel, Google Sheets).

## 2. Endpoint de Exportação

**URL:** `GET /api/admin/audit/export`
**Autenticação:** Requer Token JWT de `Owner` (Proprietário).

### Parâmetros (Query Params)
| Parâmetro | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| `start_date` | Date (YYYY-MM-DD) | Não | Data inicial do filtro. |
| `end_date` | Date (YYYY-MM-DD) | Não | Data final do filtro. |

### Exemplo de Requisição (cURL)
```bash
curl -X GET "https://api.mesaflow.com.br/api/admin/audit/export?start_date=2026-01-01" \
     -H "Authorization: Bearer SEU_TOKEN_AQUI" \
     -o audit_logs.csv
```

## 3. Estrutura do CSV
O arquivo gerado contém as seguintes colunas:

1.  **Timestamp:** Data e hora da ação (ISO 8601 UTC).
2.  **Actor:** Nome do usuário que realizou a ação.
3.  **Role:** Papel do usuário (owner, manager, etc.).
4.  **Action:** Tipo de ação (create, update, delete, login, impersonate).
5.  **Resource:** Recurso afetado (Order, Product, Settings).
6.  **Resource ID:** Identificador único do recurso.
7.  **IP Address:** Endereço IP de origem da requisição.
8.  **Details:** JSON stringificado com detalhes adicionais (ex: campos alterados).

## 4. Automação (Ingestão em SIEM)
Para automatizar a ingestão de logs no seu SIEM:
1.  Crie um script (Python/Bash) que roda periodicamente (ex: diariamente).
2.  O script deve autenticar, baixar o CSV do dia anterior (`start_date=ontem`).
3.  O script envia o CSV para o coletor do SIEM.

> **Nota de Segurança:** Proteja o Token de Acesso utilizado pelo script de automação. Recomendamos a rotação periódica das credenciais.
