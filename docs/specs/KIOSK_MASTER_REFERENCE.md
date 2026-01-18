# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 12:45:00
# 🖥️ MesaFlow Kiosk: Master Visual & QA Reference (L6)
Este documento consolida a especificação visual, comportamental e de qualidade para o módulo de Autoatendimento (Totem), integrando `KIOSK_VISUAL_CHECKLIST.md`, `KioskPage.md`, `PUBLIC_KIOSK_OFFLINE.md` e `TASK-FEAT-01`.

---

## 1. Referência Visual Interativa

### 1.1. Tela de Atração (Attract Screen)
**Rota:** `/[slug]/kiosk` | **Estado:** Idle / Deep Idle

A porta de entrada do totem. Deve ser cinematográfica, imersiva e bloquear qualquer acesso ao sistema operacional subjacente.

#### 🎨 Composição Visual
| Camada | Componente | Especificação Visual (Tailwind / CSS) | Comportamento |
| :--- | :--- | :--- | :--- |
| **Z-0** | **Background** | `bg-slate-950` (Hex: `#020617`) | Base sólida para evitar flash branco. |
| **Z-1** | **Media Layer** | Imagem/Vídeo: `object-cover`, `w-full h-full`, `opacity-30`. | **Animação:** Zoom lento (`scale-100` → `scale-110`, 20s, infinite alternate). |
| **Z-2** | **Overlay** | Gradiente: `bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent`. | Garante legibilidade do texto inferior. |
| **Z-3** | **Partículas** | 5 Elementos: `bg-orange-500/20`, `rounded-full`, `blur-xl`. | **Animação:** Movimento flutuante aleatório (X/Y) em loop infinito. |
| **Z-10** | **Logo** | Componente `<Logo size="xl" variant="light" />`. | **Entrada:** `fade-in` + `slide-down` (0.8s). |
| **Z-10** | **Hero Title** | Fonte: `Inter Black`. Tamanho: `text-7xl` (md: `text-9xl`). Cor: Branco. Destaque: "AQUI" em `#ea580c` (`text-orange-600`). | Drop Shadow: `drop-shadow-2xl`. |
| **Z-10** | **Subtítulo** | Texto: "RÁPIDO • DIGITAL • SEM FILAS". Estilo: `text-slate-300`, `uppercase`, `tracking-wide`. | - |
| **Z-20** | **CTA Button** | Container: `bg-white`, `rounded-[3rem]`, `px-16 py-8`. Sombra: `shadow-[0_20px_50px_rgba(234,88,12,0.3)]`. | **Animação:** Pulso constante (`scale-100` → `scale-105`). **Interação:** Toque em *qualquer* lugar da tela dispara. |
| **Z-20** | **Footer** | Badge: "MesaFlow Totem Intelligence v5.0". Ícone: `<Sparkles />`. Estilo: `text-white`, `opacity-30`, `font-mono`. | - |

#### 📺 Descanso de Tela (Screensaver) - *Ref: TASK-FEAT-01*
- **Gatilho:** 2 minutos de inatividade total na Tela de Atração.
- **Visual:** Carrossel de imagens full-screen (produtos em destaque) ou vídeo promocional.
- **Saída:** Toque em qualquer lugar retorna para a Tela de Atração (ou inicia o menu diretamente).

---

### 1.2. Cardápio Kiosk (Menu)
**Rota:** `/[slug]/menu?kiosk=true` | **Estado:** Active / Ordering

Interface otimizada para toque, alto contraste e decisões rápidas.

#### 🧩 Componentes
**A. KioskHeader**
- **Container:** `bg-slate-900`, `border-b border-slate-800`, `sticky top-0 z-40`.
- **Botão Voltar:** Gigante (`p-4`), `rounded-2xl`, `bg-slate-800`. Ícone `ArrowLeft` branco.
- **Identidade:** Logo do Tenant + Badge "AUTOATENDIMENTO ATIVO" (`text-orange-500`, `animate-ping` no dot).
- **Instrução:** Card à direita: "Toque nos itens para adicionar" (`bg-slate-800/50`).

**B. Grid de Produtos**
- **Layout:** Grid responsivo (2 colunas em portrait, 3 em landscape).
- **Card Produto:**
  - **Normal:** `bg-slate-900`, `border border-slate-800`.
  - **Active/Touch:** Borda muda para `border-orange-500/50`.
  - **Imagem:** Quadrada, `rounded-2xl`, `aspect-square`.
  - **Tipografia:** Nome (`text-lg`, `font-bold`, `text-white`), Preço (`text-xl`, `font-black`, `text-orange-500`).

**C. Carrinho Flutuante (Floating Cart)**
- **Posição:** `fixed bottom-0 left-0 w-full`, `z-50`.
- **Botão:** "Pílula Gigante" (`rounded-[2.5rem]`), margem `p-6`.
- **Estilo:** `bg-orange-600` (ou Primary Color do Tenant). Sombra `shadow-2xl`.
- **Conteúdo:**
  - Esquerda: Ícone `ShoppingBag` + Contador ("3 ITENS").
  - Direita: Total ("R$ 45,90") + Texto "FINALIZAR PEDIDO".
- **Animação:** `slide-in-from-bottom` (Entrada) e `scale` (Ao atualizar valor).

---

### 1.3. Checkout & Pagamento
**Rota:** `/[slug]/checkout?kiosk=true`

#### 💳 Fluxo Visual
1.  **Identificação:**
    - Input gigante (`p-4`, `text-lg`, `bg-slate-950`, `text-white`).
    - Teclado virtual nativo ou componente React (se touch-only).
2.  **Pagamento:**
    - Grid de botões quadrados grandes (`aspect-square` ou retangulares altos).
    - Ícones 32px (`Pix`, `Card`, `Cash`).
    - Estado Ativo: `bg-orange-500/10`, `border-orange-500`.
3.  **Sucesso (Feedback):**
    - Ícone Check Verde (`w-32 h-32`) com animação `pop-in` (elastic bounce).
    - Mensagem: "Pedido Confirmado!" (`text-4xl`, `font-black`).
    - Instrução: "Aguarde a chamada: [NOME]".
    - **Auto-Reset:** Barra de progresso ou texto piscante indicando retorno à Home em 5s.

---

## 2. Checklist QA Consolidado (L6)

### 🎨 Visual & Estilo (Pixel Perfect)
| Elemento | Critério de Aceite | Status |
| :--- | :--- | :---: |
| **Tema** | Dark Mode forçado (`bg-slate-950`) em todas as rotas `?kiosk=true`. | [ ] |
| **Tipografia** | Fonte `Inter`. Títulos `Black` (900). Textos de leitura `Medium` (500). | [ ] |
| **Cores** | Laranja Primário: `#ea580c`. Fundo: `#020617`. Sucesso: `#22c55e`. | [ ] |
| **Imagens** | Todas as imagens possuem `object-cover` e `rounded-2xl`. Fallback para ícone cinza se falhar. | [ ] |
| **Sombras** | Glows coloridos (`shadow-orange-500/20`) em elementos ativos. Sombras difusas em cards. | [ ] |
| **Responsividade** | Layout não quebra em: 1080x1920 (Vertical) e 1920x1080 (Horizontal). | [ ] |

### 🖱️ Interação & Comportamento
| Ação | Comportamento Esperado | Status |
| :--- | :--- | :---: |
| **Toque Global** | Na tela de atração, qualquer toque (fundo, texto, botão) inicia o fluxo. | [ ] |
| **Bloqueio** | Botão direito do mouse (Context Menu) desabilitado. Seleção de texto desabilitada. | [ ] |
| **Scroll** | Scroll elástico desabilitado (overscroll-behavior: none). Scrollbars ocultas (`no-scrollbar`). | [ ] |
| **Feedback Tátil** | Botões têm estado `active:scale-95` ou mudança de cor imediata ao toque. | [ ] |
| **Navegação** | Botão "Voltar" do header funciona. Swipe-back do navegador bloqueado. | [ ] |

### ⏱️ Temporizadores & Automação
| Funcionalidade | Regra | Status |
| :--- | :--- | :---: |
| **Inactivity Timer** | 60s sem toque → Exibe Modal "Ainda está aí?". | [ ] |
| **Auto-Reset** | 10s no Modal sem resposta → Limpa carrinho (`clearCart`) e redireciona para `/[slug]/kiosk`. | [ ] |
| **Screensaver** | 2 min na tela de Atração → Inicia Carrossel/Vídeo (TASK-FEAT-01). | [ ] |
| **Success Reset** | 5s após tela de sucesso → Redireciona para `/[slug]/kiosk`. | [ ] |

### 🛡️ Resiliência & Offline
| Cenário | Comportamento | Status |
| :--- | :--- | :---: |
| **Queda de Rede** | Exibe Toast vermelho "Sem conexão". Não trava a UI. | [ ] |
| **Página Offline** | Se carregar sem rede, exibe `/offline` com botão "Tentar Novamente" e animação de busca. | [ ] |
| **Auto-Recovery** | Script de `ping` a cada 5s tenta reconectar e recarregar a página automaticamente. | [ ] |

---

## 3. Recomendações de UX/UI (Melhoria Contínua)

### 3.1. Acessibilidade (A11y)
- **Zona de Toque:** Garantir que todos os botões tenham área clicável mínima de 48x48px (ou equivalente em rem).
- **Contraste:** Validar se o texto cinza (`text-slate-500`) sobre fundo escuro (`bg-slate-900`) passa no teste WCAG AA. Sugestão: Clarear para `text-slate-400`.
- **Modo Acessível:** Adicionar botão no rodapé para "Modo Alto Contraste" ou "Menu Baixo" (para cadeirantes, baixando os elementos interativos para a metade inferior da tela).

### 3.2. Feedback Visual
- **Skeleton Loading:** Ao carregar o cardápio, usar Skeletons escuros (`bg-slate-800` com `animate-pulse`) em vez de spinners genéricos, mantendo a imersão.
- **Adição ao Carrinho:** Animação de "partícula" voando do produto até o carrinho flutuante ao clicar em adicionar.

### 3.3. Otimização de Conversão
- **Upsell Modal:** Ao clicar em "Finalizar", exibir modal "Deseja adicionar bebida/sobremesa?" antes do checkout (se não houver bebida no carrinho).
- **Destaques:** Aumentar o tamanho dos cards de produtos "Mais Vendidos" ou "Promoção" no grid (span 2 colunas).

---

## 4. Observações Técnicas

### 4.1. Rotas e Endpoints
- **Frontend:**
  - Atração: `/[slug]/kiosk`
  - Menu: `/[slug]/menu?kiosk=true`
  - Checkout: `/[slug]/checkout?kiosk=true`
  - Offline: `/offline`
- **Backend API:**
  - Cardápio: `GET /api/{slug}/menu`
  - Pedido: `POST /api/{slug}/orders` (Payload deve conter `origin: "kiosk"`).

### 4.2. Assets Críticos
- **Imagens:** Devem ser servidas via CDN com otimização de formato (WebP/AVIF).
- **Vídeo:** O vídeo de background da tela de atração deve ser leve (< 5MB), sem áudio e em loop.

### 4.3. Fallback Offline
- O Service Worker deve cachear a estrutura do App Shell (Layout Kiosk) e o JSON do cardápio.
- Imagens devem ter placeholder local (SVG/Base64) caso o download falhe.

---
*Documento gerado para conformidade com o Protocolo INDA L6.*

