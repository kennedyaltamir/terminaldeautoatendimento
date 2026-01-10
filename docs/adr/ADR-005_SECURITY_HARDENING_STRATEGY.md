# ADR-005: Estratégia de Hardening de Segurança (RLS + Headers)

**Status:** ACEITA
**Data:** Janeiro de 2026
**Decisores:** Security Team, Architect Kernel

## Contexto
O MesaFlow opera em modelo Multi-tenant B2B, processando dados sensíveis. A segurança baseada apenas em código (filtros ORM) é propensa a erro humano. É necessário uma defesa em profundidade.

## Decisão
Implementar uma estratégia de segurança em camadas:
1.  **Isolamento de Dados:** Row-Level Security (RLS) nativo no PostgreSQL.
2.  **Proteção de Transporte:** Headers HTTP estritos (HSTS Preload, CSP Strict).
3.  **Observabilidade:** Logs estruturados e Sentry com contexto.

## Alternativas Consideradas

### 1. Isolamento Lógico via ORM (Status Quo Anterior)
- **Descrição:** Adicionar `.filter(company_id=...)` em todas as queries.
- **Contras:** Frágil. Um esquecimento expõe dados de outros clientes (IDOR).
- **Motivo do Descarte:** Risco inaceitável para Enterprise.

### 2. Isolamento Físico (Database per Tenant)
- **Descrição:** Um banco de dados para cada cliente.
- **Prós:** Isolamento total.
- **Contras:** Custo proibitivo, complexidade de migração de schema (1000 clientes = 1000 migrations).
- **Motivo do Descarte:** Inviabilidade econômica e operacional no estágio atual.

## Consequências

### Positivas
- **Segurança por Design:** O banco de dados impede vazamento de dados mesmo se a aplicação for comprometida (SQL Injection limitado ao tenant).
- **Compliance:** Atende requisitos de segregação de dados da LGPD e SOC2.
- **Reputação:** Headers de segurança garantem nota "A+" em scanners públicos.

### Negativas
- **Complexidade:** Exige gestão de sessão de banco (`SET LOCAL app.current_company_id`).
- **Compatibilidade:** RLS pode complicar queries analíticas globais (SuperAdmin).

## Compliance
Fundamental para aprovação em Due Diligence de grandes clientes e conformidade com LGPD.