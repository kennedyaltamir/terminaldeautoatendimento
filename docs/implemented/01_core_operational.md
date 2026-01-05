# 🍔 Core & Operacional

## 1. Cardápio Digital (Cliente)
- **Tecnologia:** Next.js (SSR/ISR) + Cache Redis.
- **Funcionalidades:**
    - Listagem de Categorias e Produtos.
    - Suporte a Adicionais/Opções (Obrigatórios e Opcionais).
    - Carrinho persistente (LocalStorage).
    - Check-in de Mesa via QR Code (Tokenizado).
    - Modo Kiosk (Totem) com proteção de inatividade.

## 2. KDS (Cozinha)
- **Tecnologia:** WebSockets (Redis Pub/Sub) + Polling de Fallback.
- **Funcionalidades:**
    - Visualização em tempo real de novos pedidos.
    - SLA Visual (Cores mudam conforme o tempo: Verde -> Amarelo -> Vermelho).
    - Filtros por Estação (Bar, Cozinha, Sobremesa).
    - Ações: "Iniciar Preparo", "Finalizar", "Recall" (Desfazer).
    - Gestão Rápida de Estoque (Regra 86).

## 3. App do Garçom (Mobile POS)
- **Tecnologia:** PWA (Service Workers) + Dexie.js (Offline).
- **Funcionalidades:**
    - Mapa de Mesas (Livres/Ocupadas).
    - Abertura de Mesa com nome do cliente.
    - Lançamento de pedidos (Staff Override).
    - Transferência e Junção (Merge) de mesas.
    - Fechamento de conta com calculadora de troco.
    - Notificações sensoriais (Vibração) para "Pedido Pronto" e "Chamado de Mesa".

## 4. Logística de Delivery
- **Funcionalidades:**
    - Pedidos sem mesa (Takeout/Delivery).
    - Gestão de Entregadores (Cadastro e Atribuição).
    - Despacho Inteligente.
    - Rastreamento em Tempo Real (GPS Relay via WebSocket).
    - Proof of Delivery (Código de confirmação).
