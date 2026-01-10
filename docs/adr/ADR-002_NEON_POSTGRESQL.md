# ADR-002: Uso de Neon.tech (PostgreSQL Serverless)

**Status:** ACEITA
**Data:** Outubro de 2025
**Decisores:** CTO, Infra Team

## Contexto
O sistema precisa de um banco de dados relacional robusto, compatível com PostgreSQL, que suporte escalabilidade elástica e reduza o overhead de gerenciamento de infraestrutura (backups, updates, scaling).

## Decisão
Adotamos **Neon.tech** como provedor de banco de dados PostgreSQL Serverless.

## Alternativas Consideradas

### 1. AWS RDS (PostgreSQL)
- **Prós:** Padrão de indústria, controle total.
- **Contras:** Custo fixo alto para instâncias ociosas, complexidade de configuração (VPC, Security Groups), scaling vertical lento.
- **Motivo do Descarte:** Custo inicial e complexidade operacional desproporcional para a fase de GTM.

### 2. Heroku Postgres
- **Prós:** Fácil de usar.
- **Contras:** Custo elevado por GB, tecnologia legada de containerização.
- **Motivo do Descarte:** Custo-benefício desfavorável em escala.

### 3. Supabase
- **Prós:** BaaS completo, Realtime.
- **Contras:** Vendor lock-in alto com recursos proprietários.
- **Motivo do Descarte:** Preferência por arquitetura desacoplada onde o banco é apenas infraestrutura, não plataforma de aplicação.

## Consequências

### Positivas
- **Escalabilidade:** Separação de Compute e Storage permite escalar a zero (custo baixo em dev) e escalar rápido em picos.
- **Branching:** Recurso de criar branches do banco de dados (como git) acelera o desenvolvimento e testes de CI/CD.
- **Pooling:** Suporte nativo a PgBouncer (Connection Pooling) essencial para arquitetura Serverless.

### Negativas
- **Cold Starts:** No plano gratuito/dev, pode haver latência inicial (mitigado em produção com plano pago).
- **Dependência:** Dependência de um vendor específico (embora seja Postgres padrão por baixo).

## Compliance
O Neon.tech possui certificação SOC 2 Type II, atendendo aos requisitos de segurança de fornecedores do MesaFlow.