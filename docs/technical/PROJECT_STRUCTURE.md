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
