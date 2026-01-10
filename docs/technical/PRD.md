# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 05:00:00
# 📝 Product Requirements Document (PRD) - MesaFlow

> **Produto:** MesaFlow (Sistema Operacional para Food Service)
> **Versão:** 3.1 (Enterprise & Mobile)
> **Status:** Produção / Expansão Mobile

---

## 1. Visão do Produto
O MesaFlow é uma plataforma SaaS B2B Enterprise projetada para orquestrar operações em ambientes de alto tráfego (Restaurantes, Hotéis, Estádios e Eventos).
**Diferencial:** Arquitetura Híbrida que permite a coexistência de Autoatendimento (Cliente) e Operação Assistida (Staff) na mesma comanda em tempo real.

---

## 2. Funcionalidades Core (Web & Backend)

### 2.1 Gestão de Pedidos (Order Management)
- **Autoatendimento (QR Code):** PWA para clientes pedirem e pagarem sem app.
- **Modo Kiosk (Totem):** Interface travada para terminais de autoatendimento.
- **Carrinho Persistente:** Estado salvo localmente (LocalStorage/IndexedDB).
- **Personalização:** Suporte a grupos de opções (obrigatórios/opcionais) e observações.

### 2.2 KDS (Kitchen Display System)
- **Tempo Real:** Atualização via WebSockets (< 100ms).
- **SLA Visual:** Cards mudam de cor (Verde -> Amarelo -> Vermelho) baseado no tempo.
- **Setorização:** Filtros para telas de Bar, Cozinha e Sobremesa.
- **Regra 86:** Bloqueio rápido de estoque diretamente pela tela da cozinha.
- **Modo Expedidor:** Tela de consolidação para montagem de bandejas.
- **Recall:** Capacidade de restaurar pedidos finalizados acidentalmente.

### 2.3 Motor Financeiro (Fintech)
- **Split de Pagamento:** Divisão automática de receita na fonte (Marketplace) via Mercado Pago.
- **Assinaturas (SaaS):** Gestão de planos Free/Pro via Stripe (Checkout e Portal).
- **Fidelidade (Cashback):** Carteira digital vinculada ao telefone do cliente.
- **Ledger de Gorjetas:** Registro de taxas de serviço por funcionário.

### 2.4 Logística & Delivery
- **Gestão de Frota:** Cadastro e atribuição de entregadores.
- **Rastreamento GPS:** Relay de coordenadas em tempo real para o cliente.
- **Proof of Delivery (POD):** Confirmação de entrega via código de segurança.
- **Cash Management:** Controle de dívida de entregadores (pagamentos em dinheiro).

### 2.5 Fiscal & Legal
- **Emissão NFC-e:** Integração com FocusNFe.
- **Contingência Offline:** Fila de emissão local com sincronização automática.
- **Auditoria:** Logs imutáveis de ações críticas.

### 2.6 Inteligência & Marketing
- **IA Upselling:** Motor de recomendação (Market Basket Analysis).
- **WhatsApp Automation:** Notificações transacionais (Pedido Pronto, Saiu para Entrega).
- **Gestão de Franquias:** Dashboard consolidado multi-loja.

---

## 3. Funcionalidades Mobile (App Nativo)

### 3.1 Infraestrutura
- **Autenticação Semântica:** Validação de JWT e Refresh Token com Lock de concorrência.
- **Offline-First:** Persistência local (Zustand + AsyncStorage) e reconciliação de estado.
- **Observabilidade:** Logs estruturados e integração com Sentry Nativo.

### 3.2 Mobile POS (Garçom)
- **Mapa de Mesas:** Visualização de status (Livre/Ocupada/Chamado) em tempo real.
- **Lançamento Rápido:** Busca otimizada e atalhos para itens mais vendidos.
- **Gestão de Comanda:** Transferência e Junção (Merge) de mesas.
- **Pagamento na Mesa:** Geração de QR Code Pix dinâmico no dispositivo do garçom.
- **Fila Offline:** Capacidade de lançar pedidos sem internet (Sync posterior).

### 3.3 KDS Mobile
- **Monitor de Produção:** Versão mobile do KDS para tablets/celulares.
- **Atenção Ativa:** Alertas sensoriais (Vibração) para pedidos críticos ou atrasados.
- **Controles do Operador:** Modo Silencioso e filtros de estação.

### 3.4 Hardware Integration
- **Impressão Bluetooth:** Suporte nativo a impressoras térmicas (ESC/POS).
- **Descoberta de Dispositivos:** Scan e pareamento de impressoras próximas.

---

## 4. Requisitos Não-Funcionais (NFR)

### 4.1 Performance
- **Latência:** API < 200ms, WebSocket < 100ms.
- **Escalabilidade:** Suporte a Redis Pub/Sub para múltiplos workers.
- **Build:** Docker Multi-stage para imagens leves (< 200MB).

### 4.2 Segurança
- **Zero Trust:** Validação de `company_id` em todas as queries (RLS Lógico).
- **Sanitização:** Proteção contra XSS e SQL Injection.
- **Rate Limiting:** Proteção contra DDoS e Brute-force.
- **Segredos:** Gestão via variáveis de ambiente (nunca hardcoded).

### 4.3 Governança
- **Kernel INDA:** Protocolo estrito de execução de tasks e modificação de código.
- **Fail Fast:** Abortagem imediata em caso de inconsistência ou violação de regras.
- **Documentação Viva:** Sincronização automática de docs com o código.

---

## 5. Stack Tecnológica

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.11, FastAPI, SQLAlchemy Async |
| **Frontend** | Next.js 14, Tailwind CSS, ShadcnUI |
| **Mobile** | React Native, Expo SDK 54, Zustand, NativeWind |
| **Database** | PostgreSQL 15 (Neon.tech) |
| **Cache/PubSub** | Redis (Upstash) |
| **Infra** | Docker, Render.com, Vercel |

---
*Documento Mestre de Requisitos - Atualizado em Janeiro de 2026*