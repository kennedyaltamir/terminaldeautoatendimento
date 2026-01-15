# DOMAIN: ROOT_CONFIG
# LAST_MODIFIED: 2026-01-15 02:45:00
# 📘 MASTER PROJECT SPECIFICATION — MesaFlow OS
**Caminho Físico:** `/MASTER_PROJECT_SPECIFICATION.md`  
**Versão:** 4.3 — Gold Master Candidate  
**Status de Prontidão:** `GOLD_MASTER_CANDIDATE`  
**Classificação:** Confidencial  
**Autoridade:** Fonte Única de Verdade (SSOT)
---
## 1. Contexto, Missão e Visão
O **MesaFlow OS** é uma Constituição Técnica e Operacional para ambientes de alta rotatividade e missão crítica. Seu propósito é eliminar a fricção entre o desejo do cliente e a entrega do serviço, substituindo processos manuais, fragmentados e não determinísticos por uma orquestração digital resiliente, auditável e escalável.
O sistema opera como uma camada operacional central, integrando Interfaces Web, PWA, Aplicativos Nativos e um Backend transacional determinístico com uma **Fintech embutida**.
> **Princípio Fundamental:** No MesaFlow, o pagamento não é um evento financeiro isolado — ele é o evento causal (trigger) que sincroniza cliente, staff, cozinha, logística e relatórios em tempo real.
---
## 2. Arquitetura Geral do Sistema
O MesaFlow adota o padrão **Monólito Modular Híbrido**, priorizando a consistência transacional e a facilidade de auditoria antes da fragmentação em microserviços.
### 2.1 Stack Tecnológico Oficial
| Camada | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 + FastAPI | Orquestração, regras de negócio e APIs assíncronas |
| **Frontend Web** | Next.js 14 (App Router) | Landing Pages, Admin, Dashboards e PWA Cliente |
| **Mobile** | React Native (Expo SDK 52) | Super App Operacional (Staff/KDS/Logística) |
| **Persistência** | PostgreSQL 15 (Neon) | Dados relacionais com isolamento via RLS |
| **Eventos/Real-time**| Redis Pub/Sub + WebSockets | Sincronização instantânea de status e filas |
| **Observabilidade** | Sentry | Rastreamento de erros e performance |
---
## 3. Público-Alvo e ICP (Ideal Customer Profile)
O MesaFlow é verticalizável por configuração, não por código.
*   **Food Service:** Restaurantes, Dark Kitchens, Bares e Lanchonetes.
*   **Hospitalidade:** Hotéis, Resorts e serviços de quarto (Room Service).
*   **Entretenimento:** Estádios, Arenas, Teatros e Casas de Show.
*   **Saúde:** Clínicas e Hospitais (gestão de fluxos internos e conveniência).
*   **Corporativo:** Praças de alimentação e coworkings.
---
## 4. Proposta de Valor
*   🚀 **Eficiência Operacional:** Redução de até 30% no custo de staff.
*   💰 **Aumento de Receita:** +20% médio no ticket via upselling automatizado.
*   🎯 **Precisão Total:** Eliminação de filas, erros de pedido e retrabalho.
*   🛡️ **Resiliência:** Operação contínua mesmo sob falha parcial de rede.
---
## 5. Mapa de Diretórios (Estrutura Física)
```text
/
├── MASTER_PROJECT_SPECIFICATION.md  # SSOT absoluto (Este arquivo)
├── app/               # Backend (Models, Services, API, Domain)
├── frontend/          # Web Admin + PWA Cliente (Next.js)
├── mobile/            # Aplicativo Nativo (Staff / KDS / Logística)
├── governance/        # SOBERANIA OPERACIONAL
│   ├── policies/      # LGPD, Segurança, Termos de Uso
│   ├── protocols/     # INDA, UEP, ARP (Protocolos de Execução)
│   ├── rfc/           # Request for Comments (Decisões Estruturais)
│   ├── prompts/       # Perfis cognitivos e contratos de IA
│   ├── evidence/      # Provas de auditoria (SYS, SEC, INF)
│   └── registry.xml   # Registry centralizado de estados (v4.x)
├── scripts/           # Ferramentas de Setup, Auditoria e Readiness
├── alembic/           # Migrações de schema de banco de dados
└── ignorar/           # Artefatos isolados, protótipos ou obsoletos
```
---
## 6. Segurança e Isolamento Multi-tenant
A segurança é aplicada no nível da engine de banco de dados (**Security by Design**).
*   **PostgreSQL RLS (Row-Level Security):** Cada query é automaticamente isolada pelo ID do Tenant. É impossível o vazamento de dados entre empresas, mesmo em caso de falhas na camada de aplicação.
*   **RBAC (Role-Based Access Control):** Controle de acesso rígido via JWT (Roles: Owner, Manager, Cashier, Kitchen, Driver).
*   **Integridade Financeira:** Todos os cálculos são realizados em centavos (inteiros) para evitar erros de precisão decimal.
---
## 7. Interfaces do Sistema
### 7.1 Portais Web (Next.js)
*   **Landing Pages:** SEO otimizado, SSR e conversão de leads.
*   **Painel Admin:** Gestão de cardápio, estoque, engenharia de preços e BI.
*   **PWA Cliente:** Interface leve acessada via QR Code (sem download).
### 7.2 Super App Mobile (React Native)
O aplicativo adapta sua interface dinamicamente conforme a Role do usuário:
*   **Garçom:** Comanda digital, mapa de mesas e pagamento via Pix na mesa.
*   **Cozinha (KDS):** Fila de produção organizada por SLA e prioridade.
*   **Logística/Entregador:** Roteirização e confirmação de entrega.
*   **Gerente:** Visão tática, alertas de KPIs e liberação de descontos/estornos.
### 7.3 Monitores Públicos
*   Exibição de senhas (chamada) e status de prontidão (Pass/Expedição).
---
## 8. Integrações e Infraestrutura
*   **Pagamentos:** Mercado Pago (Pix/Split) e Stripe (SaaS Billing).
*   **Comunicação:** WhatsApp Business API (Notificações transacionais).
*   **Marketplaces:** Integração Inbound com iFood via Webhooks.
*   **Hospedagem:** Render.com (App) e Neon.tech (Database Serverless).
*   **Hardware:** Suporte a impressoras térmicas ESC/POS via Bluetooth/Rede.
---
## 9. Governança, Compliance e Qualidade
O projeto é regido pelo **Protocolo INDA** (Inspection, Normalization, Decision, Action).
*   **Quality Gates:** Bloqueio físico de deploy caso os requisitos de segurança (SEC) ou infraestrutura (INF) não sejam atingidos.
*   **Auditoria:** Todas as evidências de integridade são armazenadas em `/governance/evidence/`.
---
## 10. Estados de Prontidão (Registry)
### 🟡 EM VALIDAÇÃO (GOLD MASTER)
*   **SEC-04:** Auditoria de ambiente em execução.
*   **INF-01:** Healthcheck aguardando inicialização do servidor.
*   **OBS-01:** Teste de Sentry aguardando patch de ambiente.
### 🟢 HOMOLOGADOS
*   **SEC-01:** Isolamento RLS validado e testado.
*   **APP-01:** Contexto ORM e Migrações sincronizados.
*   **SYS-01:** Estrutura de diretórios auditada e limpa.
---
## 11. Limites do Sistema (Out of Scope)
O MesaFlow OS **NÃO** executa:
1.  Custódia direta de valores financeiros (delegado ao Gateway).
2.  ERP contábil/fiscal completo (foco em operação e fluxo).
3.  Venda de hardware proprietário.
4.  IA generativa de cardápios (IA restrita a predição de demanda e upsell).
---
## 12. Modelo de Negócio
*   **SaaS:** Assinatura mensal por unidade/ponto de venda.
*   **Fintech:** Take rate (taxa transacional) capturada via split automatizado no momento do pagamento.
---
## 13. Roadmap Imediato (Execução Ativa)
1.  **Ativação Gold Master:** Execução do script `activate_gold_master.py` para patch de ambiente e validação final.
2.  **Deploy:** Liberação para produção após sucesso do MRC.
---
## 14. Declaração Final
O **MesaFlow OS** não é apenas um software, mas uma infraestrutura operacional auditável, construída para escalar com segurança, clareza e honestidade técnica.
**MesaFlow Technology — Engineered for Stability, Sealed for Market.**
