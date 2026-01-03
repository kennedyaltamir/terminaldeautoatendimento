# 🚀 MesaFlow

> **Sistema Operacional de Autoatendimento para Food Service.**
> Transforme mesas em pontos de venda inteligentes. Sem filas, sem apps, sem espera.

## 🎯 Público-Alvo
*   🍔 **Hamburguerias e Fast-food** (Giro rápido, KDS vital).
*   🍺 **Bares e Pubs** (Pedidos recorrentes, divisão de conta).
*   🍕 **Pizzarias** (Adicionais complexos, Delivery híbrido).

## ✨ Funcionalidades Principais

### 📱 Para o Cliente (Cardápio Digital)
*   **Zero App:** Acesso instantâneo via QR Code (PWA).
*   **UX Nativa:** Navegação fluida, busca instantânea e filtros.
*   **Carrinho Inteligente:** Edição de itens, persistência offline e upsell.
*   **Pagamento:** Pix Automático (Mercado Pago) ou Checkout na entrega.
*   **Social:** Divisão de conta (Split Bill) integrada.

### 👨‍🍳 Para a Cozinha (KDS)
*   **Tempo Real:** Pedidos chegam em milissegundos (WebSocket).
*   **Gestão de SLA:** Cores indicam atrasos (Verde/Amarelo/Vermelho).
*   **Controle Total:** Botão "86" (Esgotar item) e Recall de pedidos.
*   **Impressão:** Suporte nativo a impressoras térmicas USB/Bluetooth.

### 🏢 Para a Gestão (Admin)
*   **Mapa de Sala:** Layout visual das mesas (Drag & Drop).
*   **Cardápio:** Gestão completa de produtos, adicionais e estoque.
*   **Financeiro:** Relatórios de vendas e controle de caixa.

## 🛠️ Tech Stack
*   **Backend:** Python 3.11+ (FastAPI, SQLAlchemy, WebSockets).
*   **Frontend:** Next.js 14 (App Router, Tailwind CSS, Lucide Icons).
*   **Database:** PostgreSQL.
*   **Infra:** Docker Ready.

## 🚀 Como Rodar

1.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    cd frontend && npm install
    ```

2.  **Configurar Banco de Dados:**
    Crie um arquivo `.env` na raiz com `DATABASE_URL`.
    ```bash
    python scripts/seed.py  # Popula com dados de teste
    ```

3.  **Iniciar Sistema:**
    ```bash
    python run.py
    ```
    *   Frontend: `http://localhost:3000`
    *   Backend: `http://localhost:8000`

## 🧪 Testes
O projeto possui uma suíte robusta de testes automatizados.
```bash
python -m pytest




# 🚀 MesaFlow

> **O Sistema Operacional de Autoatendimento para Food Service.**
> Transforme mesas em pontos de venda inteligentes. Sem filas, sem apps, sem espera.

## ✨ O que o MesaFlow faz hoje?
O MesaFlow é uma plataforma SaaS B2B que elimina a necessidade de garçons para anotar pedidos. O cliente escaneia um QR Code, abre o cardápio, personaliza seu prato e paga. O pedido cai instantaneamente na cozinha (KDS).

### 🛠️ Tech Stack
- **Backend:** Python 3.11 (FastAPI), SQLAlchemy (Async), PostgreSQL, WebSockets.
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide React.
- **Real-time:** Comunicação bidirecional via WebSockets para KDS e Chamadas.

### 📱 Funcionalidades Ativas
- **Cardápio Digital:** Com busca, filtros por tags e lógica de adicionais.
- **KDS (Kitchen Display System):** Monitor de produção com cronômetro de SLA e Recall.
- **Gestão de Mesas:** Mapa de sala visual com Drag & Drop.
- **Híbrido:** Suporte total para Mesa (Comanda) e Delivery.
- **Landing Page:** Site institucional profissional integrado.



# 🚀 MesaFlow

> **Sistema Operacional de Autoatendimento para Food Service.**
> Transforme mesas em pontos de venda inteligentes. Sem filas, sem apps, sem espera.

## 🎯 O que o MesaFlow faz?
O MesaFlow é uma plataforma SaaS B2B que elimina a necessidade de garçons para anotar pedidos.
1.  **Cliente:** Escaneia QR Code -> Faz Pedido -> Paga (Pix/Cartão).
2.  **Cozinha (KDS):** Recebe pedido em tempo real -> Prepara -> Notifica.
3.  **Gestão:** Controla estoque, faturamento e taxas automaticamente.

## ✨ Funcionalidades (Fase 3 Concluída)

### 📱 Para o Cliente (Cardápio Digital)
*   **PWA (App Web):** Funciona como app nativo (instalável) sem download da loja.
*   **UX Fluida:** Busca instantânea, filtros por tags e carrinho persistente.
*   **Pagamento Split:** O valor é dividido automaticamente entre o Restaurante e a Plataforma (SaaS).

### 👨‍🍳 Para a Operação (KDS & Estoque)
*   **Ficha Técnica:** Baixa automática de ingredientes (ex: 1 Burger = 0.18kg Carne + 1 Pão).
*   **Monitor KDS:** Alertas sonoros, cronômetro de SLA e separação por praça (Bar/Cozinha).
*   **Gestão de Mesas:** Mapa de sala visual com status em tempo real.

### 🏢 Para o Dono (Admin)
*   **Branding:** Personalização completa de cores, logo e banner.
*   **Financeiro:** Relatórios de vendas, ticket médio e controle de taxas.
*   **Segurança:** Proteção contra ataques de força bruta e spam de pedidos.

## 🛠️ Tech Stack
*   **Backend:** Python 3.11+ (FastAPI, SQLAlchemy, SlowAPI).
*   **Frontend:** Next.js 14 (App Router, Tailwind CSS, Framer Motion).
*   **Database:** PostgreSQL.
*   **Infra:** Docker Ready.

## 🚀 Como Rodar

1.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    cd frontend && npm install
    ```

2.  **Configurar Banco de Dados:**
    Certifique-se que o PostgreSQL está rodando e o `.env` está configurado.
    ```bash
    python scripts/seed.py  # Popula com dados de teste (Login: admin@mesaflow.com / 123456)
    ```

3.  **Iniciar Sistema:**
    Use o script gerenciador para subir Backend e Frontend juntos:
    ```bash
    python run.py
    ```
    *   **Frontend:** `http://localhost:3000`
    *   **Backend:** `http://localhost:8000`

## 🧪 Testes
O projeto possui uma suíte robusta de testes automatizados.
```bash
python -m pytest