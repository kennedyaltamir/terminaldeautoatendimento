# 🧭 Matriz de Comportamento Esperado do Sistema (L6)
**Status:** SSOT (Single Source of Truth) para Validação de QA
**Data:** 15/01/2026

Este documento define o comportamento padrão esperado para cada interação crítica no sistema MesaFlow. Utilize esta matriz para validar se a realidade (o que acontece na tela) condiz com a especificação (o que deveria acontecer).

---

## 1. Módulo Cliente (Cardápio Digital)
**Rota:** `/[slug]/menu`

| Elemento / Evento | Ação do Usuário | Comportamento Visual Esperado (Frontend) | Comportamento de Sistema (Backend/WS) |
| :--- | :--- | :--- | :--- |
| **Card de Produto** | Clique | Abrir modal de detalhes do produto com foto, descrição e opções. | N/A (Dados já carregados). |
| **Botão "Adicionar" (Modal)** | Clique | Fechar modal, animar ícone do carrinho (shake/pulse), exibir toast "Adicionado com sucesso". | Atualizar estado local (CartContext). |
| **Botão "Ver Carrinho"** | Clique | Abrir drawer/modal do carrinho listando itens, subtotal e total. | N/A. |
| **Input "Cupom"** | Digitar + Enter | Exibir mensagem de validação ("Aplicado" ou "Inválido") e atualizar total. | POST `/api/cart/validate-coupon`. |
| **Botão "Enviar Pedido"** | Clique | Exibir spinner de carregamento, bloquear interface. Ao sucesso: redirecionar para `OrderStatusView`. | POST `/api/[slug]/orders` (201 Created) -> Disparar WS `new_order`. |
| **Status do Pedido** | (Passivo) | Atualizar badge de status (ex: de "Pendente" para "Preparando") sem refresh da página. | Receber WS `order_update`. |

---

## 2. Módulo Cozinha (KDS)
**Rota:** `/admin/[slug]/kitchen`

| Elemento / Evento | Ação do Usuário | Comportamento Visual Esperado (Frontend) | Comportamento de Sistema (Backend/WS) |
| :--- | :--- | :--- | :--- |
| **Novo Pedido (Evento)** | (Passivo) | Novo card aparece na primeira posição da coluna "Pendente". Tocar som de alerta ("Ding"). | Receber WS `new_order`. |
| **Botão "Iniciar Preparo"** | Clique | Card move instantaneamente para coluna "Em Preparo". Cor da borda muda (Cinza -> Azul). | PATCH `/api/orders/{id}` (status=preparing) -> Broadcast WS `order_update`. |
| **Botão "Pronto"** | Clique | Card move para coluna "Pronto" (ou some, dependendo do filtro). Cor muda para Verde. | PATCH `/api/orders/{id}` (status=ready) -> Broadcast WS `order_update`. |
| **Filtro "Cozinha/Bar"** | Clique | Lista de pedidos é filtrada para mostrar apenas itens da estação selecionada. | Filtragem local ou refetch com query param. |
| **Botão "Tela Cheia"** | Clique | Interface ocupa todo o monitor, ocultando barras do navegador. | API Fullscreen do Browser. |

---

## 3. Módulo Garçom (POS)
**Rota:** `/admin/[slug]/waiter`

| Elemento / Evento | Ação do Usuário | Comportamento Visual Esperado (Frontend) | Comportamento de Sistema (Backend/WS) |
| :--- | :--- | :--- | :--- |
| **Mesa Livre (Card Cinza)** | Clique | Abrir modal "Abrir Mesa". Solicitar nome do cliente e quantidade de pessoas. | - |
| **Botão "Abrir Mesa"** | Clique (no modal) | Card da mesa muda para Verde (Ocupada). Redirecionar para tela de pedido da mesa. | POST `/api/tables/{id}/open`. |
| **Mesa Ocupada (Card Verde)** | Clique | Navegar para tela de detalhes da mesa (`/pos/[id]`). Carregar itens consumidos. | GET `/api/session/{token}`. |
| **Chamado de Cliente** | (Passivo) | Card da mesa pisca em Vermelho/Amarelo. Ícone de sino aparece. | Receber WS `waiter_call`. |
| **Botão "Fechar Conta"** | Clique | Exibir resumo da conta, opções de gorjeta e métodos de pagamento. | - |
| **Botão "Pagamento Pix"** | Clique | Gerar QR Code Pix na tela do garçom para o cliente escanear. | POST `/api/payment` (provider=mercadopago). |

---

## 4. Módulo Expedição & Delivery
**Rota:** `/admin/[slug]/delivery`

| Elemento / Evento | Ação do Usuário | Comportamento Visual Esperado (Frontend) | Comportamento de Sistema (Backend/WS) |
| :--- | :--- | :--- | :--- |
| **Aba "A Retirar"** | (Passivo) | Listar pedidos com status `ready` e tipo `delivery`. | Polling ou WS. |
| **Botão "Despachar"** | Clique | Abrir modal de seleção de entregador (Motoqueiro). | GET `/api/employees?role=driver`. |
| **Confirmar Despacho** | Clique | Pedido move para aba "Em Rota". | PATCH `/api/orders/{id}` (status=delivering, driver_id=...). |
| **Botão "WhatsApp"** | Clique | Abrir API do WhatsApp com mensagem pré-preenchida para o cliente. | `window.open('https://wa.me/...')`. |

---

## 5. Módulo Administrativo (Dashboard)
**Rota:** `/admin/[slug]/dashboard`

| Elemento / Evento | Ação do Usuário | Comportamento Visual Esperado (Frontend) | Comportamento de Sistema (Backend/WS) |
| :--- | :--- | :--- | :--- |
| **Filtro de Data** | Clique (ex: "Hoje") | Gráficos e Cards de KPI atualizam os valores para o período selecionado. | GET `/api/metrics?period=today`. |
| **Card "Faturamento"** | Hover (Mouse) | Exibir tooltip com detalhamento ou comparação com período anterior. | - |
| **Lista "Top Produtos"** | Scroll | Carregar mais itens se houver paginação (Infinite Scroll). | - |

---

## 6. Fluxo de Login & Segurança
**Rota:** `/admin/login`

| Elemento / Evento | Ação do Usuário | Comportamento Visual Esperado (Frontend) | Comportamento de Sistema (Backend/WS) |
| :--- | :--- | :--- | :--- |
| **Input E-mail/Senha** | Digitar | Campos devem aceitar texto e mascarar senha. | - |
| **Botão "Entrar"** | Clique | Botão exibe estado de loading (spinner). Se sucesso: redirecionar para Dashboard. Se erro: exibir alerta vermelho. | POST `/api/auth/token`. Armazenar JWT no LocalStorage/Cookies. |
| **Token Expirado** | (Passivo) | Ao tentar acessar rota protegida, redirecionar automaticamente para `/admin/login`. | Interceptor Axios (401 -> Logout). |

---

*Documento gerado para auditoria de conformidade L6.*
