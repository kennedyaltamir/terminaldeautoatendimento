# 📱 Documentação Funcional de Interface (UI/UX) — MesaFlow OS
> **Versão:** 5.2 (Enriched Gold Master)
> **Data:** 16/01/2026
> **Status:** AUDITED & EXPANDED
> **Autoridade:** Optimus Kernel L6

Este documento detalha a especificação funcional, comportamental e crítica de todas as interfaces do sistema, servindo como referência absoluta para QA, Desenvolvimento e Design.

---

## 1. Web — Área Pública & Institucional

### 1.1 Landing Page (SaaS Conversion)
**Rota:** `/`
**Arquivo:** `frontend/src/app/page.tsx`

*   **Propósito:** Porta de entrada comercial e conversão. O objetivo é transformar visitantes em leads qualificados ou contas de teste (PLG) através de uma narrativa visual de alta performance.
*   **Elementos Interativos:**
    *   `Hero CTA`: Botão "Começar Grátis" (Primary) e "Ver Demo" (Secondary/Outline).
    *   `Pricing Toggle`: Switch Mensal/Anual com animação de desconto (-20%).
    *   `Simulator`: Componente interativo (Cliente -> Cozinha) com feedback visual de WebSocket simulado.
    *   `Lead Magnet`: Modal de intenção de saída (Exit Intent) capturando e-mail.
    *   `Floating Widget`: Botão WhatsApp flutuante (Z-Index alto).
*   **Estados:**
    *   `Interactive`: Animações de scroll (Framer Motion) ativas.
    *   `Loading`: Otimizado via SSG (Static Site Generation). LCP < 1.2s.
*   **Fluxos:**
    *   CTA Principal -> `/admin/register`
    *   Login -> `/admin/login`
    *   Demo -> Modal de seleção de vertical -> Redireciona para `/[slug]/menu`.
*   **Observações Críticas (SEO/Performance):**
    *   **Core Web Vitals:** Imagens devem usar `next/image` com `priority` no Hero.
    *   **SEO:** JSON-LD estruturado para "SoftwareApplication".
    *   **Acessibilidade:** Todos os botões devem ter `aria-label`.

### 1.2 Trust Center & Status
**Rota:** `/trust`, `/trust/status`
**Arquivo:** `frontend/src/app/trust/page.tsx`

*   **Propósito:** Transparência radical para clientes Enterprise. Exibe a saúde da infraestrutura e conformidade legal/segurança em tempo real.
*   **Elementos Interativos:**
    *   `Status Indicators`: Beacons (Verde/Amarelo/Vermelho) para API, DB e Redis.
    *   `Compliance Badges`: Links para documentos de LGPD e PCI-DSS.
    *   `Refresh Button`: Re-trigger manual do healthcheck.
*   **Integrações:**
    *   Consome endpoint `/api/health` (INF-01).
*   **Estados:**
    *   `Loading`: Skeleton nos cards de status.
    *   `Error`: Degradação graciosa (exibe "Status Desconhecido" em vez de crash).
*   **Melhoria Sugerida:** Implementar histórico de uptime (gráfico de barras dos últimos 30 dias).

---

## 2. Web — Experiência do Cliente Final (Tenant)

### 2.1 Menu Digital (Client PWA)
**Rota:** `/[slug]/menu`
**Arquivo:** `frontend/src/app/[slug]/menu/page.tsx`

*   **Propósito:** Interface de pedidos self-service. Deve ser extremamente rápida, "app-like" e resistente a falhas de rede intermitentes (Offline-First visual).
*   **Elementos Interativos:**
    *   `CategoryNav`: Scroll horizontal com "spy-scroll" (ativa a categoria visível).
    *   `ProductCard`: Imagem (Lazy), Preço, Botão "Adicionar".
    *   `ProductModal`: Seleção de opcionais (Radio/Checkbox), Observações (Textarea), Contador de quantidade.
    *   `CartWidget`: Floating Action Button (FAB) com total e contador de itens.
    *   `OrderStatusView`: Stepper em tempo real (WebSocket) e Mapa (Leaflet).
*   **Estados:**
    *   `Loading`: Skeleton de categorias e produtos (evita CLS).
    *   `Empty`: "Nenhum produto disponível" (se estoque zerado).
    *   `Offline`: Banner "Modo Leitura - Sem Conexão" (Service Worker ativo).
*   **Fluxos:**
    *   Seleção -> Modal de Opções -> Carrinho -> Checkout (Pix/Card).
    *   Pós-venda -> Acompanhamento (WebSocket) -> Avaliação (NPS).
*   **Integrações:**
    *   **WebSocket:** Escuta canal `mesaflow:[slug]` para atualizações de status.
    *   **Maps:** Renderiza rota de entrega se `order_type=delivery`.
*   **Observações Críticas:**
    *   **Optimistic UI:** Adicionar ao carrinho deve ser instantâneo visualmente.
    *   **Cache:** Uso agressivo de `localStorage` para persistir carrinho em caso de refresh.

### 2.2 Kiosk Mode (Totem)
**Rota:** `/[slug]/kiosk`
**Arquivo:** `frontend/src/app/[slug]/kiosk/page.tsx`

*   **Propósito:** Tela de atração para totens físicos. Previne burn-in e convida o cliente.
*   **Elementos Interativos:**
    *   `Touch Area`: A tela inteira é um botão gigante.
*   **Comportamento:**
    *   Loop de vídeo/imagem em background.
    *   **Auto-Reset:** Timer de inatividade (60s) no Menu redireciona de volta para cá.
    *   **Bloqueio:** CSS `user-select: none` e bloqueio de menu de contexto.

---

## 3. Web — Painel Administrativo (Backoffice)

### 3.1 Dashboard Gerencial
**Rota:** `/admin/[slug]/dashboard`
**Arquivo:** `frontend/src/app/admin/[slug]/dashboard/page.tsx`

*   **Propósito:** Visão tática da operação. Decisões baseadas em dados em tempo real.
*   **Elementos Interativos:**
    *   `Date Range Picker`: Filtros (Hoje, 7 dias, Mês).
    *   `KPI Cards`: Faturamento, Ticket Médio, CAC.
    *   `Sales Chart`: Gráfico de área (Recharts) com tooltip interativo.
    *   `Export Button`: Download de CSV/PDF.
*   **Estados:**
    *   `Loading`: Skeleton nos cards e gráficos.
    *   `Error`: "Falha ao carregar métricas" com botão de retry.
*   **Integrações:**
    *   API de Métricas (`/api/admin/metrics`).
*   **Performance:**
    *   Dados pesados carregados via `Promise.all` para paralelismo.

### 3.2 Gestão de Estoque (Inventory)
**Rota:** `/admin/[slug]/inventory`
**Arquivo:** `frontend/src/app/admin/[slug]/inventory/page.tsx`

*   **Propósito:** Controle de insumos e Ficha Técnica.
*   **Regra de Negócio (Regra 86):** Se um ingrediente zerar, todos os produtos vinculados devem ser automaticamente pausados no cardápio.
*   **Elementos Interativos:**
    *   `Stock Table`: Inputs de edição inline para quantidade.
    *   `Recipe Modal`: Vínculo Produto <-> Ingredientes (Select com busca).
    *   `Low Stock Alert`: Badge visual para itens abaixo do mínimo.
*   **Fluxos:**
    *   Edição Rápida -> Salvar (Optimistic Update) -> Sync Backend.
*   **Melhoria Sugerida:** Adicionar histórico de movimentação (Log) por ingrediente.

---

## 4. Web — Operação Crítica (Mission Critical)

### 4.1 Kitchen Display System (KDS)
**Rota:** `/admin/[slug]/kitchen`
**Arquivo:** `frontend/src/app/admin/[slug]/kitchen/page.tsx`

*   **Propósito:** Substituir impressoras de cozinha. Orquestração de produção de alta velocidade.
*   **Elementos Interativos:**
    *   `OrderCard`: Timer progressivo (Verde < 10m, Amarelo < 20m, Vermelho > 20m).
    *   `Action Buttons`: "Iniciar Preparo", "Pronto" (Áreas de clique grandes para touch).
    *   `Station Filter`: Abas (Cozinha, Bar, Sobremesa).
    *   `Recall Button`: Desfazer última ação (Undo).
*   **Integrações:**
    *   **WebSocket:** Recebimento passivo de novos pedidos (Zero Refresh).
    *   **Audio:** Alerta sonoro ("Ding") via `AudioContext`.
*   **Resiliência:**
    *   **Heartbeat:** Monitora conexão WS. Se cair, exibe banner "Desconectado" e tenta reconectar.
    *   **Local State:** Mantém pedidos na tela mesmo se a internet cair momentaneamente.

### 4.2 Ponto de Venda (PDV/Counter)
**Rota:** `/admin/[slug]/counter`
**Arquivo:** `frontend/src/app/admin/[slug]/counter/page.tsx`

*   **Propósito:** Operação de caixa rápida (High throughput).
*   **Elementos Interativos:**
    *   `Product Grid`: Botões grandes com fotos.
    *   `Cart Sidebar`: Lista de itens, descontos, total.
    *   `Payment Modal`: Seleção de método (Dinheiro/Pix/Cartão), Calculadora de Troco.
*   **UX:**
    *   **Keyboard First:** Atalhos para busca (`/`), pagamento (`F2`), finalizar (`Enter`).
    *   **Layout Denso:** Menos whitespace, mais informação por pixel.
*   **Integrações:**
    *   **Impressão:** Aciona driver RawBT ou Browser Print ao finalizar.
    *   **Fiscal:** Dispara emissão de NFC-e em background.

---

## 5. Mobile — Aplicativo Nativo (React Native)

### 5.1 Login & Auth Gate
**Arquivo:** `mobile/src/screens/auth/LoginScreen.tsx`

*   **Propósito:** Autenticação segura e persistente.
*   **Elementos:**
    *   `EmailInput`, `PasswordInput`: Teclado correto (`email-address`, `default`).
    *   `LoginButton`: Estado de loading (Spinner).
*   **Segurança:**
    *   Tokens salvos em `SecureStore`.
    *   **AuthGate:** Componente que valida a semântica do JWT (expiração) antes de montar a stack de navegação.
*   **Fluxo:** Login -> `AuthGate` -> Redirecionamento baseado em Role (Driver -> DriverDashboard, Waiter -> WaiterDashboard).

### 5.2 Waiter Dashboard (Garçom)
**Arquivo:** `mobile/src/screens/waiter/WaiterDashboard.tsx`

*   **Propósito:** Gestão de salão em movimento.
*   **Elementos:**
    *   `TableGrid`: Mesas com status codificado por cor (Livre=Verde, Ocupada=Vermelho, Pagando=Amarelo).
    *   `NotificationBadge`: Contador de chamados de clientes (Sino).
    *   `FAB`: Botão "Nova Comanda Avulsa".
*   **Offline/Latência:**
    *   **SyncQueue:** Ações realizadas sem internet são enfileiradas e enviadas quando a conexão retorna.
    *   **Optimistic Updates:** A mesa muda de cor imediatamente ao toque, revertendo apenas se o backend rejeitar.

### 5.3 Order Entry (Comanda Mobile)
**Arquivo:** `mobile/src/screens/orders/OrderEntryScreen.tsx`

*   **Propósito:** Lançamento de pedidos na mesa com velocidade.
*   **Elementos:**
    *   `SearchBar`: Busca local de produtos (Fuse.js) para zero latência.
    *   `ProductListItem`: Stepper de quantidade (+/-).
    *   `CartSummary`: Barra inferior fixa com total e botão "Enviar".
*   **UX:**
    *   **Haptic Feedback:** Vibração leve ao adicionar itens.
    *   **Keyboard Avoidance:** A lista não deve ser coberta pelo teclado virtual.

### 5.4 Driver Dashboard (Logística)
**Arquivo:** `mobile/src/screens/dashboard/DriverDashboard.tsx`

*   **Propósito:** Gestão de entregas para motoboys próprios.
*   **Elementos:**
    *   `Tabs`: "A Retirar" (Cozinha) vs "Em Rota" (Comigo).
    *   `OrderCard`: Endereço, Nome, Botão "Navegar" (Deep link Waze/Maps).
    *   `SwipeAction`: Deslizar para confirmar entrega.
*   **Integrações:**
    *   **GPS:** Envio de telemetria em background (Throttled 3s) para o backend.
    *   **WebSocket:** Recebe evento "Pedido Pronto" e toca som específico.
*   **Segurança:**
    *   Validação de `driver_id` no backend para impedir roubo de pedidos entre motoboys.

### 5.5 Printer Debug (Ferramenta)
**Arquivo:** `mobile/src/screens/waiter/PrinterDebugScreen.tsx`

*   **Propósito:** Diagnóstico de hardware em campo.
*   **Elementos:**
    *   `DeviceList`: Lista de dispositivos Bluetooth pareados.
    *   `TestButton`: Envia buffer ESC/POS de teste.
*   **Funcionalidade:**
    *   Scan Bluetooth Low Energy (BLE).
    *   Teste de alinhamento, acentuação e corte de papel.

---

## 6. Considerações Transversais de Qualidade

1.  **Consistência Visual:** Todos os componentes (Web/Mobile) consomem os tokens do Design System (`colors.orange.600`, `spacing.md`) definidos em `frontend/tailwind.config.ts` e `mobile/src/theme`.
2.  **Tratamento de Erros:**
    *   **Web:** `GlobalError.tsx` captura falhas não tratadas.
    *   **Mobile:** `ErrorBoundary` envolve a navegação para evitar crash total do app.
3.  **Acessibilidade (a11y):**
    *   **Web:** Navegação por teclado (Tabindex) e ARIA labels em ícones.
    *   **Mobile:** Áreas de toque mínimas de 44x44dp e suporte a Dynamic Type (tamanho de fonte).
4.  **Internacionalização (i18n):** Estrutura preparada para chaves (atualmente hardcoded PT-BR, mas arquiteturalmente desacoplada via `dictionaries.ts`).

---
*Documentação gerada e validada pelo Kernel MesaFlow L6.*

