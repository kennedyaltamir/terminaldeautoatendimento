📘 MesaFlow: The Master Technical Bible

Versão do Sistema: 3.0 (Enterprise Edition)
Data de Compilação: Janeiro/2026
Classificação: Documentação Técnica & Estratégica
Stack: Python (FastAPI) + Next.js (React) + PostgreSQL + Redis

1. 🎯 Visão Executiva (Product Vision)

O MesaFlow é um Sistema Operacional (SaaS) para ambientes de alto tráfego (Restaurantes, Hotéis, Estádios). Diferente de cardápios digitais passivos, ele atua como um orquestrador de operações em tempo real.

1.1 A Proposta de Valor (UVP)

Arquitetura Híbrida: Permite a coexistência de Autoatendimento (Cliente pede via QR Code) e Atendimento Assistido (Garçom lança no Mobile POS) na mesma comanda, em tempo real.

Fintech Embutida: Atua como subadquirente, processando pagamentos via Pix/Cartão e realizando o Split de Pagamento (Comissão do SaaS vs Receita do Restaurante) na fonte.

Logística Integrada: Possui módulo nativo de despacho e App para Entregadores com rastreamento GPS e gestão de caixa.

1.2 Segmentação de Mercado (Verticalização)

O sistema utiliza uma arquitetura polimórfica para atender diferentes nichos:

Gastro: Mesas, Comandas, KDS.

Hotelaria: Room Service (Mesa = Quarto), Agendamento.

Eventos: Venda no Assento (Mesa = Cadeira), Fila Expressa.

Corporativo: Coffee Breaks, Pagamento Centralizado.

2. 🏗️ Arquitetura de Software

O sistema segue o padrão de Monolito Modular (Modular Monolith), priorizando simplicidade operacional e consistência de dados sobre a complexidade de microserviços prematuros.

2.1 Tech Stack
Camada	Tecnologia	Detalhes Técnicos
Backend	Python 3.11+	FastAPI (Async/Await), Pydantic v2, SQLAlchemy 2.0.
Frontend	Next.js 14	App Router, Server Actions, TypeScript Strict, Tailwind CSS.
Database	PostgreSQL 15	Hospedado no Neon.tech (Serverless). Uso de Connection Pooling.
Real-time	Redis	Pub/Sub para WebSockets (KDS/GPS) e Caching L2 (Menu).
Offline	Dexie.js	IndexedDB wrapper para persistência local no PWA (Sync Engine).
Infra	Docker	Containers otimizados (Multi-stage build). Deploy no Render.com.
2.2 Padrões de Design (Design Patterns)

Multi-tenancy (Isolamento Lógico): Utilização de Row-Level Security (RLS) simulado. Todas as queries filtram obrigatoriamente por company_id.

Factory Pattern: Utilizado nos serviços de Pagamento (PaymentFactory) e Fiscal (FiscalFactory) para permitir troca de provedores (ex: Mercado Pago -> Stripe) sem refatorar o core.

Adapter Pattern: Camada de abstração para hardware (Impressoras Térmicas ESC/POS e ZPL).

Repository Pattern (Implícito): Acesso a dados abstraído via SQLAlchemy Sessions injetadas (Depends(get_db)).

2.3 Segurança (Hardening)

Zero Trust: Validação de company_id em todos os endpoints.

Rate Limiting: Implementado via SlowAPI (Redis) para prevenir DDoS e Brute-force.

Sanitização: Middleware de limpeza de HTML para prevenir XSS Stored.

Auditoria: Tabela audit_logs imutável registrando todas as operações de escrita críticas (Quem, Quando, O Quê).

3. 🧩 Módulos do Sistema (Core Features)
3.1 Cardápio Digital & Pedidos (Client-Side)

Carrinho Persistente: Estado salvo no LocalStorage/IndexedDB.

Modo Kiosk: Interface travada para totens de autoatendimento com timeout de inatividade.

Upselling (IA): Motor de recomendação baseado em Market Basket Analysis (Co-ocorrência de produtos).

3.2 KDS (Kitchen Display System)

SLA Visual: Cards mudam de cor (Verde -> Amarelo -> Vermelho) conforme o tempo de preparo.

Setorização: Filtros persistentes para telas de Bar, Cozinha ou Sobremesa.

Regra 86 (Estoque): Bloqueio imediato de itens esgotados diretamente pela tela da cozinha.

Modo Expedidor: Tela de consolidação para montagem de bandejas.

3.3 Mobile POS (App do Garçom)

Gestão de Mesas: Mapa visual, Abertura/Fechamento, Transferência e Junção (Merge) de mesas.

Token de Segurança: PIN de 10 dígitos para recuperação de sessão de mesa.

Notificações Sensoriais: Vibração e Som no dispositivo ao receber chamados ou pratos prontos.

3.4 Logística & Delivery

App do Entregador: PWA simplificado para aceite de rotas.

Rastreamento: Relay de coordenadas GPS via WebSocket para o cliente final.

Cash Management: Ledger de controle de dinheiro na mão do entregador e prestação de contas.

POD (Proof of Delivery): Confirmação de entrega via código de segurança.

3.5 Motor Financeiro

Assinaturas (SaaS): Integração profunda com Stripe (Checkout, Portal, Webhooks) para gestão de planos Free/Pro.

Split de Pagamento: Divisão de receita na fonte via Mercado Pago OAuth.

Fidelidade: Cashback calculado automaticamente e vinculado ao telefone do cliente.

4. 🗺️ Roadmap & Status Atual

O projeto concluiu a Fase 8 (Excelência Operacional) e está iniciando a Fase 9 (Expansão & Ecossistema).

✅ Concluído (Production Ready)

Core: Auth, Multi-tenancy, CRUDs básicos.

Operação: KDS 2.0, App Garçom, Impressão Térmica/ZPL.

Financeiro: Split Pix, Assinaturas Stripe, Ledger de Gorjetas.

Logística: App Driver, Rastreamento, POD.

Inteligência: WhatsApp Automation (Evolution API), IA Upselling.

🔄 Em Andamento (Fase 9 - Ecossistema)

Marketing: Motor de Promoções e Cupons (Regras de desconto no carrinho).

Developer Experience: Documentação OpenAPI (Swagger) pública e Webhooks de saída (Webhooks UI).

Monitoramento: Painel de status de integrações (WhatsApp/Fiscal) no frontend.

🔮 Futuro (Backlog Enterprise)

Fiscal Real: Homologação NFC-e/SAT com contingência offline.

Hub de Delivery: Integração iFood/Rappi (Middleware de pedidos).

Mobile Nativo: Migração dos PWAs para React Native (Lojas Apple/Google).

Gestão Avançada: Tenant Impersonation (Suporte) e Feature Flags.

5. ⚙️ Guia de Operações (DevOps)
5.1 Pipeline de CI/CD (GitHub Actions)

Backend Job: Roda pytest com banco PostgreSQL isolado (Docker Service).

Frontend Job: Roda npm run build para validação de tipagem e linting.

Política: Green Build. O deploy para Render/Vercel só ocorre se todos os testes passarem.

5.2 Scripts de Manutenção (scripts/)

O projeto possui uma CLI robusta para manutenção:

python scripts/maintenance/seed.py: Popula o banco com dados de demonstração (Gastro, Hotel, Evento).

python scripts/maintenance/fix_db_schema.py: Aplica correções emergenciais de schema sem Alembic.

python scripts/security/security_audit.py: Roda pentest automatizado (IDOR, XSS, Rate Limit).

python atualizar.py: Automação de refatoração baseada em IA.

5.3 Monitoramento

Sentry: Captura de exceções fullstack.

Health Check: Endpoint /api/health monitora latência do DB e conexão Redis.

6. 🧪 Estratégia de Testes
Backend (Pytest)

Unitários: Lógica de negócios (cálculo de split, validação de estoque).

Integração: Testes de API (TestClient) simulando fluxos completos (Pedido -> Pagamento -> KDS).

Mocks: Serviços externos (Stripe, WhatsApp, Redis) são mockados com AsyncMock.

Frontend (Playwright)

E2E: Simulação de navegadores reais.

Cenários Críticos:

Fluxo de Pedido (Cliente).

Fluxo de KDS (Cozinha).

Fluxo de Delivery (Admin + Driver).

7. 📝 Convenções de Código

Cabeçalhos: Todo arquivo deve iniciar com # FILE: caminho/do/arquivo.ext.

Tipagem: Python com Type Hints estritos. TypeScript sem any.

Commits: Padrão Conventional Commits (feat:, fix:, chore:).

Integridade Financeira: Valores monetários sempre usam Decimal (Python) e inteiros/centavos (Stripe/MP), nunca float.

Fim do Documento Mestre.
Este arquivo deve ser mantido atualizado a cada grande release.

# 📘 MesaFlow: The Master Technical Bible (v3.0)

## 1. Visão Geral
O MesaFlow é um ecossistema SaaS B2B All-in-One para Food Service e Hospitalidade. Sua arquitetura é projetada para ser **Híbrida** (Online/Offline) e **Multi-tenant** (Isolamento total de dados).

## 2. Constituição Técnica (Regras Inegociáveis)
1.  **Integridade Financeira:** É terminantemente proibido o uso de `float` para valores monetários. Deve-se usar `Decimal` (Python) ou `number` (centavos no Frontend) para evitar erros de arredondamento IEEE 754.
2.  **Zero Trust Multi-tenancy:** Toda e qualquer query ao banco de dados deve conter o filtro explícito por `company_id`. O vazamento de dados entre tenants é considerado falha crítica de segurança.
3.  **Async First:** Operações de I/O (Banco, Redis, APIs externas) devem ser assíncronas para garantir a alta disponibilidade do loop de eventos do FastAPI.
4.  **IDs Primários:** Utilizamos `GUID` (UUID v4) para chaves primárias, garantindo compatibilidade entre SQLite (testes) e PostgreSQL (produção).

## 3. Arquitetura de Dados
A hierarquia de recursos segue o fluxo:
`Company` -> `Category` -> `Product` -> `OptionGroup` -> `Option`.
- **Mapeamento Externo:** Produtos possuem o campo `external_id` para sincronização com iFood/Rappi.
- **Origem do Pedido:** Pedidos possuem o campo `origin` (`mesaflow`, `ifood`, `rappi`).

## 4. Stack Tecnológica
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0 (Async), Pydantic v2.
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Dexie.js.
- **Infra:** PostgreSQL (Neon), Redis (Upstash), Docker.

---
*Documento atualizado em Janeiro de 2026 - Fase 9 (Enterprise).*
# 📘 MesaFlow: The Master Technical Bible (v3.1)

## 1. Visão Geral da Arquitetura
O MesaFlow utiliza o padrão **Monolito Modular**. Diferente de microserviços, mantemos a simplicidade de deploy, mas com separação lógica rigorosa entre domínios (Fintech, Logistics, Menu, Auth).

## 2. Camada de Dados e Multi-tenancy
### 2.1 Isolamento Lógico (RLS)
Embora o PostgreSQL suporte RLS nativo, utilizamos **Isolamento via Aplicação**:
- Toda tabela possui `company_id`.
- O `current_user` extraído do JWT injeta o `company_id` em todas as queries via dependência do FastAPI.
- **Risco:** Queries sem filtro. **Solução:** Auditoria via `security_audit.py`.

### 2.2 Tipagem de IDs
- **GUID (UUID v4):** Chave primária para todas as entidades. Evita ataques de enumeração de IDs e facilita a sincronização offline (o ID pode ser gerado no cliente sem colisão).

## 3. Regras de Ouro da Engenharia
- **Valores Monetários:** Use `Decimal(10, 2)`. Nunca use `float` para dinheiro.
- **Estado do Pedido:** O fluxo é unidirecional: `pending` -> `accepted` -> `preparing` -> `ready` -> `delivered`.
- **Hardware:** Abstração via `EscPosBuilder`. O backend gera o binário, o frontend despacha via protocolo `rawbt:`.

## 4. Segurança e Criptografia
- **JWT:** HS256 com expiração de 30 min (Access) e 7 dias (Refresh).
- **Webhooks:** Assinatura HMAC-SHA256 obrigatória no header `X-MesaFlow-Signature`.
- **Senhas:** Hashing via `bcrypt` com salt dinâmico.

---
