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

# 🧭 Matriz de Comportamento Esperado do Sistema (L6)
**Status:** SSOT (Single Source of Truth) para Validação de QA
**Versão:** 2.0 — Cobertura Total (38 Páginas)
**Data:** 15/01/2026

Este documento detalha o comportamento esperado para cada interação em todas as telas do ecossistema MesaFlow.

---

## 1. Módulo Público & Cliente (PWA/Landing)

### 1.1. Landing Page (`/`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Começar Agora" | Clique | Navega para `/admin/register`. |
| Botão "Ver Demo" | Clique | Abre `DemoModal` com opções de segmentos. |
| Seletor de Idioma | Clique | Altera o dicionário de textos (PT/EN/ES) sem recarregar a página. |
| Botão "Login" | Clique | Navega para `/admin/login`. |

### 1.2. Cardápio Digital (`/[slug]/menu`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Card de Produto | Clique | Abre `ProductModal`. Se o produto tiver recomendações, abre `UpsellModal` após fechar o primeiro. |
| Botão "Adicionar" | Clique | Adiciona item ao `CartContext`. Se for a primeira vez, solicita nome do cliente. |
| Botão "Ver Carrinho" | Clique | Abre drawer lateral com resumo do pedido. |
| Botão "Chamar Garçom" | Clique | Abre `ServiceModal`. Envia sinal via WS para o App do Garçom e KDS. |
| Botão "Minha Comanda" | Clique | Abre `ComandaView` listando todos os pedidos da sessão atual da mesa. |
| Parâmetro `?order=ID` | Load | Carrega diretamente a `OrderStatusView` para o pedido específico (Deep Link). |

### 1.3. Kiosk / Totem (`/[slug]/kiosk`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Tela de Atração | Toque | Inicia sessão e navega para o menu em modo totem. |
| Timer de Inatividade | Passivo | Após 60s sem toque, exibe `InactivityModal`. Se não houver resposta em 10s, volta para tela de atração. |

### 1.4. Monitor Público (`/[slug]/monitor`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Lista de Pedidos | Passivo | Atualiza via WS. Pedidos `ready` aparecem em destaque (Verde) com alerta sonoro. |

---

## 2. Módulo Administrativo (Backoffice)

### 2.1. Dashboard (`/admin/[slug]/dashboard`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Filtros (Hoje/7D/Mês) | Clique | Dispara `getDashboardMetrics` e atualiza gráficos do Recharts. |
| Botão "Exportar CSV" | Clique | Gera e baixa arquivo com histórico de vendas do período. |
| Card de KPI | Hover | Exibe tendência percentual em relação ao período anterior. |

### 2.2. Gestão de Cardápio (`/admin/[slug]/menu`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Toggle "Disponível" | Clique | Altera `is_available` no banco. Produto fica opaco no menu do cliente instantaneamente. |
| Botão "Ficha Técnica" | Clique | Abre `RecipeModal` para vincular ingredientes ao produto. |
| Botão "Importar iFood" | Clique | Solicita URL do iFood e popula categorias/produtos automaticamente. |

### 2.3. Gestão de Mesas (`/admin/[slug]/tables`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Gerar QR Codes" | Clique | Abre visualização de impressão com todos os QRs das mesas ativas. |
| Card de Mesa | Drag | Altera `position_x/y` no banco para salvar o layout do salão. |
| Botão "Fechar Mesa" | Clique | Calcula total + gorjeta, gera Pix (se configurado) e encerra `TableSession`. |

### 2.4. Auditoria Financeira (`/admin/[slug]/audit/financial`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Tabela Ledger | Load | Exibe cadeia de hashes imutável. Se houver quebra de integridade, exibe alerta vermelho. |
| Botão "Fix Orphan" | Clique | Reconcilia transação do gateway que não possui registro no banco local. |

---

## 3. Módulo Operacional (Staff)

### 3.1. KDS / Cozinha (`/admin/[slug]/kitchen`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Card de Pedido | Clique | Avança status: Pendente -> Preparando -> Pronto. |
| Atalhos (1, 2, 3...) | Teclado | Avança o status do pedido na posição correspondente da grade. |
| Botão "Voz" | Clique | Ativa reconhecimento de voz. Comando "Pedido X pronto" avança o status. |

### 3.2. App do Garçom (`/admin/[slug]/waiter`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Transferir" | Clique | Move todos os pedidos de uma mesa para outra. Se a destino estiver ocupada, oferece "Merge". |
| Botão "Dividir Conta" | Clique | Abre `SplitBillModal`. Permite pagar valor exato, dividir por pessoas ou por itens. |

### 3.3. App do Entregador (`/admin/[slug]/driver`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Pegar Pedido" | Clique | Atribui `driver_id` ao pedido e muda status para `delivering`. |
| Botão "Waze/Maps" | Clique | Abre aplicativo externo com coordenadas do endereço de entrega. |
| Botão "Finalizar" | Clique | Solicita código de confirmação (se configurado) e encerra entrega. |

---

## 4. Fluxos Transversais

### 4.1. Segurança & Auth
| Evento | Comportamento Esperado |
| :--- | :--- |
| Login Sucesso | Salva JWT no LocalStorage e redireciona baseado na Role (Kitchen -> KDS, Driver -> DriverApp). |
| Erro 401 (API) | Interceptor dispara `refresh_token`. Se falhar, limpa storage e força redirecionamento para `/login`. |
| Acesso Cross-tenant | O RLS do PostgreSQL bloqueia o retorno de dados, resultando em 404 ou lista vazia, mesmo com token válido. |

### 4.2. Resiliência Offline
| Evento | Comportamento Esperado |
| :--- | :--- |
| Queda de Internet | Exibe `NetworkStatus` (Banner Vermelho). Permite continuar navegando no menu (Cache). |
| Pedido Offline | Salva no `MesaFlowDB` (IndexedDB). Sincroniza automaticamente ao detectar volta da rede. |

---
*Documento gerado pelo Kernel de Governança MesaFlow.*
