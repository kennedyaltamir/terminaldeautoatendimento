# 🧠 Conceito e Regras de Negócio: MesaFlow

Este documento descreve a lógica de funcionamento do ecossistema MesaFlow, detalhando os atores, fluxos e regras que regem a plataforma.

---

## 1. Atores do Sistema

### 👤 Cliente Final
*   **Objetivo:** Comer/Beber rápido, sem filas e sem erros.
*   **Interface:** Web App (PWA) acessado via QR Code.
*   **Ações:** Visualizar cardápio, personalizar itens, chamar garçom, pagar conta, acompanhar status.

### 🤵 Garçom / Staff
*   **Objetivo:** Atender com hospitalidade e resolver problemas, não apenas anotar.
*   **Interface:** App do Garçom (Mobile).
*   **Ações:** Abrir mesas, lançar pedidos adicionais, transferir mesas, validar pagamentos em dinheiro.

### 👨‍🍳 Cozinha / Bar (Produção)
*   **Objetivo:** Preparar pedidos na ordem correta e dentro do tempo (SLA).
*   **Interface:** KDS (Tablet/Monitor).
*   **Ações:** Visualizar fila, iniciar preparo, finalizar prato, notificar garçom, pausar itens (estoque).

### 🛵 Entregador (Logística)
*   **Objetivo:** Levar o pacote do ponto A ao B com eficiência.
*   **Interface:** App do Motorista (Mobile).
*   **Ações:** Aceitar rota, visualizar endereço/mapa, coletar assinatura/código de entrega.

### 👔 Gestor / Dono
*   **Objetivo:** Controle financeiro e operacional.
*   **Interface:** Painel Admin (Desktop).
*   **Ações:** Configurar cardápio, ver métricas, gerenciar equipe, configurar taxas e pagamentos.

---

## 2. Fluxos Principais

### Fluxo A: Pedido na Mesa (Dine-in)
1.  **Check-in:** Cliente escaneia QR Code -> Sistema valida token da mesa -> Cria/Recupera Sessão.
2.  **Pedido:** Cliente adiciona itens -> Envia para cozinha.
3.  **Produção:** KDS toca som -> Cozinheiro aceita -> Prepara -> Finaliza.
4.  **Entrega:** Garçom recebe notificação (vibração) -> Leva à mesa.
5.  **Pagamento:** Cliente paga via Pix no celular (Baixa automática) OU chama garçom para pagar em dinheiro/maquininha.

### Fluxo B: Delivery Próprio
1.  **Pedido:** Cliente acessa link público em casa -> Preenche endereço -> Paga online.
2.  **Despacho:** Gerente vê pedido "Pronto" no painel -> Seleciona Entregador.
3.  **Rota:** Entregador recebe notificação -> Abre Waze -> Entrega.
4.  **Confirmação:** Entregador digita código fornecido pelo cliente (POD) para finalizar.

---

## 3. Regras de Negócio Críticas

### 📦 Estoque e Ficha Técnica
*   **Regra 86:** Se o estoque de um produto chegar a zero, ele deve desaparecer automaticamente de todos os cardápios digitais ativos imediatamente (via WebSocket).
*   **Composição:** A baixa de estoque ocorre nos *ingredientes* (ex: 1 Burger = 1 Pão + 180g Carne), não apenas no produto final.

### 💰 Financeiro (Split)
*   O sistema opera como um facilitador de pagamentos.
*   Ao receber um Pix de R$ 100,00:
    *   O Gateway (Mercado Pago) divide o valor na fonte.
    *   A taxa da plataforma (ex: 2%) vai para a conta do MesaFlow.
    *   O restante vai para a conta do Restaurante.
*   Isso evita bitributação e garante a receita do SaaS.

### 🔄 Sincronização Híbrida
*   Uma mesa pode ter múltiplos clientes conectados simultaneamente ("Multiplayer").
*   Se o Cliente A adiciona uma Coca-Cola, o Cliente B (e o Garçom) devem ver essa Coca-Cola na comanda em tempo real.
*   O fechamento da conta bloqueia novos pedidos para aquela sessão.