
# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-11 12:10:00

# 📋 Registro de Dívida Técnica — MesaFlow
Este documento traduz as falhas da auditoria em itens acionáveis de engenharia.

## 🔐 Segurança (Prioridade Máxima)
### TD-SEC-001: Migração para PostgreSQL RLS
- **Descrição:** Implementar Row-Level Security nativo para isolar `company_id` na camada de dados.
- **Status:** ✅ RESOLVIDO (TASK-SEC-01).

### TD-SEC-002: Auditoria de God Mode Imutável
- **Descrição:** Mover logs de impersonation para uma tabela protegida ou serviço externo de log.
- **Status:** ABERTO.

### TD-SEC-003: Auditoria AST de Variáveis Intermediárias
- **Descrição:** O auditor atual não detecta `val = data.status; order.status = val`.
- **Risco:** Baixo (Requer má fé ou erro complexo).
- **Status:** ABERTO (Monitorar).

## 🚀 Escalabilidade
### TD-ESC-001: Migração iFood para Webhooks
- **Descrição:** Substituir o polling de 30s por uma arquitetura orientada a eventos (Inbound Webhooks).
- **Status:** ✅ RESOLVIDO (TASK-ESC-01).

## 🤖 QA & Automação (Optimus v6 Roadmap)
### TD-QA-001: Input Strategy Engine
- **Descrição:** Substituir o preenchimento genérico "Test" por uma engine contextual (`email`, `password`, `cpf`) com casos de borda.
- **Status:** ABERTO (Planejado v6).

### TD-QA-002: Video Chapterization
- **Descrição:** Gerar arquivo `chapters.json` sincronizando timestamps do vídeo com eventos do log INDA.
- **Status:** ABERTO (Planejado v6).

### TD-QA-003: Safe Click & Rollback
- **Descrição:** Implementar estratégia de clique em botões de navegação com rollback automático (voltar para a página anterior) para validar links sem destruir estado.
- **Status:** ABERTO (Planejado v6).

## 📱 Mobile & Hardware
### TD-MOB-001: Otimização do Global Clock
- **Descrição:** Aumentar o intervalo do pulso ou implementar suspensão inteligente para economizar bateria.
- **Status:** ✅ RESOLVIDO (TASK-MOB-01).

### TD-MOB-002: Drivers de Impressão Nativos
- **Descrição:** Implementar suporte direto a Bluetooth/USB sem depender do RawBT.
- **Status:** ABERTO.

## 💰 Fintech
### TD-FIN-001: Abstração de Provedor (Multi-gateway)
- **Descrição:** Implementar Circuit Breaker e segundo provedor na `PaymentFactory`.
- **Status:** ABERTO.

### TD-FIN-002: Sincronia de Precisão Decimal
- **Descrição:** Garantir que o Frontend trate valores como strings ou inteiros (centavos) para evitar erros de float.
- **Status:** ✅ RESOLVIDO (TASK-FIN-01).

