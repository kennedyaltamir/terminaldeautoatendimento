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