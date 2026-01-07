# 📂 Estrutura do Projeto MesaFlow

Guia de navegação para desenvolvedores e IAs.

## 1. Raiz
- `run.py`: Script mestre para iniciar Backend + Frontend simultaneamente (Dev).
- `atualizar.py`: Ferramenta de automação para aplicar patches de código.
- `gerartxt.py`: Gerador de contexto otimizado para LLMs.

## 2. Backend (`app/`)
O cérebro da aplicação. FastAPI + SQLAlchemy.

- `main.py`: Entrypoint. Configura rotas, CORS e Sentry.
- `models.py`: **Definição do Banco de Dados.** Todas as tabelas estão aqui.
- `schemas.py`: **Contratos de Dados (Pydantic).** Validação de entrada/saída.
- `routers/`: Controladores divididos por domínio.
    - `public.py`: Rotas do cliente final (Cardápio, Check-in).
    - `admin_*.py`: Rotas do painel de gestão (protegidas).
    - `webhooks.py`: Receptores de eventos externos (Stripe/MP).
- `services/`: Lógica de negócio complexa.
    - `payment_service.py`: Orquestração de pagamentos e Split.
    - `stock_service.py`: Regra 86 e baixa de estoque.
    - `fiscal/`: Adapter pattern para emissão de notas.
- `core/`: Configurações base (Segurança, Cache, Limites SaaS).

## 3. Frontend (`frontend/`)
A face da aplicação. Next.js 14 (App Router).

- `src/app/`: Roteamento baseado em arquivos.
    - `[slug]/menu/`: **O Cardápio Digital.**
    - `[slug]/kiosk/`: **Modo Totem.**
    - `admin/[slug]/`: **Painel Administrativo.**
        - `kitchen/`: KDS.
        - `waiter/`: App do Garçom.
        - `delivery/`: Gestão de Logística.
- `src/components/`: Blocos de UI reutilizáveis.
    - `menu/`: Componentes específicos do cardápio (Modal de Produto, Carrinho).
    - `admin/`: Componentes de gestão (Gráficos, Tabelas).
- `src/lib/`: Utilitários.
    - `api.ts`: Cliente HTTP centralizado (Fetch wrapper).
    - `printer/`: Motor de impressão ESC/POS binário.
    - `smartpos.ts`: Gerador de Deep Links para maquininhas.
- `src/context/`: Estado global (Carrinho, WebSocket).

## 4. Scripts (`scripts/`)
Automação e manutenção.

- `setup/`: Instalação e verificação de ambiente.
- `maintenance/`: Migrações, Seeds e Limpeza.
- `security/`: Auditorias e correções de segurança.
- `functional/`: Testes manuais de funcionalidades específicas.
- `tests/`: **Suíte de Testes Automatizados (Pytest).**
# 📂 Estrutura do Projeto MesaFlow

## 🧠 Backend (`app/`)
- `services/ifood_service.py`: Motor de polling e ingestão de pedidos do marketplace.
- `services/webhook_dispatcher.py`: Motor de disparo de notificações externas com lógica de retry.
- `services/fiscal/`: Camada de abstração para emissão de notas (Adapter Pattern).
- `core/docs.py`: Configurações de metadados para o Swagger.

## 🎨 Frontend (`frontend/src/`)
- `hooks/useFiscalSync.ts`: Worker de sincronização de notas fiscais offline.
- `hooks/useOfflineSync.ts`: Worker de sincronização de pedidos offline.
- `lib/db.ts`: Definição do banco de dados local (Dexie.js/IndexedDB).
- `components/admin/WebhookManager.tsx`: Interface de gestão de integrações.
- `components/admin/WhatsappStatus.tsx`: Monitor de saúde da API de mensagens.

## 🧪 Testes (`scripts/tests/`)
- `test_promotion_flow_e2e.py`: Validação ultra-rígida do motor de promoções.
- `test_fiscal_contingency_e2e.py`: Simulação de queda de internet e sincronização fiscal.
- `test_outgoing_webhooks.py`: Validação de integridade e assinatura HMAC.
- `test_ifood_integration.py`: Simulação de ingestão de pedidos externos.

---
