
[[MESAFLOW_BEGIN:docs/TECHNICAL_DEBT_REGISTER.md]]
# 📋 Registro de Dívida Técnica — MesaFlow

Este documento traduz as falhas da auditoria em itens acionáveis de engenharia.

## 🔐 Segurança (Prioridade Máxima)
### TD-SEC-001: Migração para PostgreSQL RLS
- **Descrição:** Implementar Row-Level Security nativo para isolar `company_id` na camada de dados.
- **Risco:** Vazamento massivo de dados (LGPD).
- **Status:** ABERTO.

### TD-SEC-002: Auditoria de God Mode Imutável
- **Descrição:** Mover logs de impersonation para uma tabela protegida ou serviço externo de log.
- **Status:** ABERTO.

## 🚀 Escalabilidade
### TD-ESC-001: Migração iFood para Webhooks
- **Descrição:** Substituir o polling de 30s por uma arquitetura orientada a eventos (Inbound Webhooks).
- **Risco:** Saturação de I/O e queda de performance em escala.
- **Status:** ABERTO.

## 📱 Mobile & Hardware
### TD-MOB-001: Otimização do Global Clock
- **Descrição:** Aumentar o intervalo do pulso ou implementar suspensão inteligente para economizar bateria.
- **Status:** ABERTO.

### TD-MOB-002: Drivers de Impressão Nativos
- **Descrição:** Implementar suporte direto a Bluetooth/USB sem depender do RawBT.
- **Status:** ABERTO.

## 💰 Fintech
### TD-FIN-001: Abstração de Provedor (Multi-gateway)
- **Descrição:** Implementar Circuit Breaker e segundo provedor na `PaymentFactory`.
- **Status:** ABERTO.

### TD-FIN-002: Sincronia de Precisão Decimal
- **Descrição:** Garantir que o Frontend trate valores como strings ou inteiros (centavos) para evitar erros de float.
- **Status:** ABERTO.
[[MESAFLOW_END]]
                ]]]]><![CDATA[></Content>
            </File>
            <File>
                <Path>docs/ARCHITECTURAL_DECISIONS.md</Path>
                <Content><![CDATA[
[[MESAFLOW_BEGIN:docs/ARCHITECTURAL_DECISIONS.md]]
# 🏗️ Architectural Decision Records (ADR)

## ADR-001: Priorização de Hardening sobre Features
**Data:** 2026-01-08  
**Status:** APROVADO  
**Contexto:** Auditoria estratégica identificou fragilidades Enterprise.  
**Decisão:** Interromper o desenvolvimento de novas funcionalidades de marketing/UI até que os débitos de Segurança (RLS) e Escala (Webhooks) sejam quitados.

## ADR-002: Manutenção Temporária da Governança Rígida
**Data:** 2026-01-08  
**Status:** APROVADO  
**Decisão:** Manter os protocolos XML e INDA atuais, apesar do overhead.  
**Motivo:** A rigidez é necessária para garantir que a migração crítica para RLS seja executada sem erros de filtragem. A simplificação da governança será a última fase do hardening.

## ADR-003: Estratégia de Precisão Financeira
**Data:** 2026-01-08  
**Status:** APROVADO  
**Decisão:** O padrão de comunicação financeira entre Front e Back será em **Centavos (Inteiros)**.  
**Motivo:** Eliminar a deriva de centavos causada pelo tipo `number` do JavaScript.
[[MESAFLOW_END]]
                ]]]]><![CDATA[></Content>
            </File>
            <File>
                <Path>docs/TASKS.md</Path>
                <Content><![CDATA[
[[MESAFLOW_BEGIN:docs/TASKS.md]]
# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 07:15:00
# 📋 Backlog Mestre de Tarefas: MesaFlow

---

## 🔴 PRIORIDADE ZERO: Hardening de Infraestrutura (Audit 2026-01)
- [ ] **[TASK-SEC-01]** Implementar PostgreSQL Row-Level Security (RLS) em todas as tabelas core.
- [ ] **[TASK-ESC-01]** Migrar integração iFood de Polling para Webhooks (Inbound).
- [ ] **[TASK-FIN-01]** Refatorar trânsito financeiro para Centavos (Inteiros) no Frontend.
- [ ] **[TASK-MOB-01]** Otimizar Global Clock para modo de economia de energia.

---

## 🚀 Próximas Prioridades (Sprint Mobile & Deep Tech)