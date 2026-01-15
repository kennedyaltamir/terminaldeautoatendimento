# 🧭 Matriz de Comportamento Esperado do Sistema (L6)
**Status:** SSOT (Single Source of Truth) para Validação de QA
**Data:** 15/01/2026

Este documento define o comportamento padrão esperado para **TODAS** as telas do sistema MesaFlow. Utilize esta matriz para validar se a realidade (o que acontece na tela) condiz com a especificação.

---

## 1. Módulo Público & Cliente

### 1.1. Landing Page & Trust
**Rotas:** `/`, `/trust`, `/trust/status`, `/trust/security`, `/offline`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Links de Navegação** | Clique | Scroll suave para seção ou navegação para página interna. | - |
| **Botão "Começar"** | Clique | Redirecionar para `/admin/register`. | - |
| **Botão "Login"** | Clique | Redirecionar para `/admin/login`. | - |
| **Status Indicator** | Load | Exibir "Operacional" (Verde) ou "Instabilidade" (Vermelho). | GET `/health` |

### 1.2. Cardápio Digital (Cliente)
**Rota:** `/[slug]/menu`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Categorias (Nav)** | Clique | Scroll suave até a seção da categoria selecionada. | - |
| **Barra de Busca** | Digitar | Filtrar lista de produtos em tempo real. | Filtragem Local. |
| **Card de Produto** | Clique | Abrir modal de detalhes. | - |
| **Botão "Adicionar"** | Clique | Fechar modal, animar ícone do carrinho, Toast de sucesso. | Atualizar Contexto. |
| **Botão "Ver Carrinho"** | Clique | Abrir drawer do carrinho com itens e subtotal. | - |
| **Input "Cupom"** | Enter | Exibir "Aplicado" ou "Inválido". Atualizar total. | POST `/api/cart/validate`. |
| **Botão "Enviar"** | Clique | Loading spinner -> Redirecionar para Status. | POST `/api/orders`. |

### 1.3. Kiosk (Totem) & Monitor
**Rotas:** `/[slug]/kiosk`, `/[slug]/monitor`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Tela de Atração** | Toque | Navegar para `/menu?kiosk=true`. | - |
| **Inatividade** | Timer | Exibir modal "Ainda está aí?". Resetar se não houver resposta. | Timer Local. |
| **Card "Pronto"** | (Passivo) | Card aparece na coluna verde com animação de destaque. Tocar som. | WS `order_update`. |

---

## 2. Módulo de Autenticação

**Rotas:** `/admin/login`, `/admin/register`, `/admin/forgot-password`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Input Email/Senha** | Digitar | Aceitar texto. Validar formato no blur. | - |
| **Botão "Entrar"** | Clique | Spinner. Sucesso: Dashboard. Erro: Shake + Msg Vermelha. | POST `/api/auth/token`. |
| **Link "Esqueci Senha"** | Clique | Navegar para tela de recuperação. | - |
| **Botão "Criar Conta"** | Clique | Spinner. Sucesso: Dashboard (Auto-login). | POST `/api/auth/register`. |

---

## 3. Módulo Operacional (Staff)

### 3.1. KDS (Cozinha)
**Rota:** `/admin/[slug]/kitchen`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Novo Pedido** | (Passivo) | Card entra em "Pendente". Som de alerta. | WS `new_order`. |
| **Botão "Preparar"** | Clique | Card move para "Preparando". Borda Azul. | PATCH status=`preparing`. |
| **Botão "Pronto"** | Clique | Card some (ou move para pronto). | PATCH status=`ready`. |
| **Filtro Estação** | Clique | Mostrar apenas itens da estação (Cozinha/Bar). | Filtro Local. |
| **Botão "Resumo"** | Clique | Abrir sidebar com contagem de itens agrupados. | Agregação Local. |

### 3.2. Expedição
**Rota:** `/admin/[slug]/expeditor`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Pedido Pronto** | (Passivo) | Card aparece na lista. | WS `order_update`. |
| **Botão "Despachar"** | Clique | Card some. Toast "Entregue". | PATCH status=`delivered`. |

### 3.3. Garçom (POS) & Mesas
**Rotas:** `/admin/[slug]/waiter`, `/admin/[slug]/waiter/pos/[id]`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Mesa Livre** | Clique | Modal "Abrir Mesa". | - |
| **Confirmar Abertura** | Clique | Mesa fica Verde (Ocupada). Vai para POS. | POST `/api/tables/open`. |
| **Adicionar Item** | Clique | Item vai para carrinho volátil. | - |
| **Enviar Pedido** | Clique | Limpa carrinho. Toast Sucesso. | POST `/api/orders`. |
| **Botão "Conta"** | Clique | Modal de Fechamento com totais. | GET `/api/session`. |
| **Botão "Dividir"** | Clique | Modal de Split (Igual ou Por Item). | Cálculo Local. |
| **Pagamento Pix** | Clique | Gerar QR Code na tela. | POST `/api/payment`. |
| **Pagamento Dinheiro** | Clique | Calculadora de Troco. Confirmar -> Mesa Livre. | POST `/api/tables/close`. |

### 3.4. Delivery & Driver
**Rotas:** `/admin/[slug]/delivery`, `/admin/[slug]/driver`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Aba "A Retirar"** | (Passivo) | Lista pedidos prontos para entrega. | Polling/WS. |
| **Botão "Despachar"** | Clique | Modal de seleção de Motoboy. | GET `/api/employees`. |
| **Confirmar** | Clique | Pedido vai para "Em Rota". | PATCH `/api/dispatch`. |
| **Botão "Waze"** | Clique | Abrir app de mapa externo. | Deep Link. |
| **Botão "Finalizar"** | Clique | Pedido some. Status "Entregue". | PATCH `/api/complete`. |

---

## 4. Módulo Administrativo (Backoffice)

### 4.1. Dashboard & Histórico
**Rotas:** `/admin/[slug]/dashboard`, `/admin/[slug]/history`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Filtro Data** | Clique | Atualizar gráficos e KPIs. | GET `/api/metrics`. |
| **Botão "Ver" (Tabela)** | Clique | Modal com detalhes do pedido e itens. | - |
| **Botão "Fiscal"** | Clique | Tentar emitir NFC-e. Status muda (Processando -> Emitida). | POST `/api/fiscal/emit`. |

### 4.2. Cardápio & Estoque
**Rotas:** `/admin/[slug]/menu`, `/admin/[slug]/inventory`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Toggle Disponível** | Clique | Produto fica cinza/ativo imediatamente. | PATCH `/api/products`. |
| **Botão "Novo"** | Clique | Modal de cadastro. | - |
| **Salvar Produto** | Clique | Fecha modal, atualiza lista. | POST/PUT `/api/products`. |
| **Input Estoque** | Blur | Atualiza quantidade. Se < Min, fica vermelho. | PATCH `/api/ingredients`. |

### 4.3. Configurações & Equipe
**Rotas:** `/admin/[slug]/settings`, `/admin/[slug]/team`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Input Cor** | Change | Preview do tema muda em tempo real. | - |
| **Botão "Salvar"** | Clique | Toast "Configurações salvas". | PATCH `/api/company`. |
| **Botão "Novo Membro"** | Clique | Modal de convite (Email/Role). | POST `/api/employees`. |
| **Botão "Excluir"** | Clique | Confirmação -> Remove da lista. | DELETE `/api/employees`. |

### 4.4. Auditoria Financeira
**Rota:** `/admin/[slug]/audit/financial`

| Elemento | Ação | Comportamento Visual (Frontend) | Sistema (Backend) |
| :--- | :--- | :--- | :--- |
| **Botão "Atualizar"** | Clique | Spinner -> Recarrega Ledger e Conciliação. | GET `/api/audit/*`. |
| **Botão "Corrigir"** | Clique | (Em transação órfã) Cria entrada no Ledger. | POST `/api/audit/fix`. |

---

*Documento gerado para auditoria de conformidade L6.*
