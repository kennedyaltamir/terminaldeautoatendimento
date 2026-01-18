# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 12:30:00
# 🖥️ Kiosk Visual & Interaction Specification (L6 Standard)
Este documento consolida a documentação técnica e define o checklist visual rigoroso para a homologação dos Totens de Autoatendimento MesaFlow.
---
## 1. Referência Documental (Source of Truth)
Os seguintes artefatos definem a implementação atual do subsistema Kiosk:
### 1.1. Estrutura & Layout
- **Attract Screen:** `frontend/src/app/[slug]/kiosk/page.tsx`
- **Layout Wrapper:** `frontend/src/app/[slug]/kiosk/layout.tsx` (Inactivity Timer)
- **Header Component:** `frontend/src/components/Kiosk/KioskHeader.tsx`
### 1.2. Lógica de Negócio
- **Menu Client:** `frontend/src/app/[slug]/menu/MenuClient.tsx` (Modo `?kiosk=true`)
- **Checkout Client:** `frontend/src/app/[slug]/checkout/CheckoutClient.tsx` (Modo `?kiosk=true`)
- **Inactivity Modal:** `frontend/src/components/kiosk/InactivityModal.tsx`
---
## 2. Checklist Visual Detalhado
### 🟢 TELA 1: ATRAÇÃO (Attract Screen)
**Rota:** `/[slug]/kiosk`
#### 2.1. Background & Atmosfera
- [ ] **Fundo:** `bg-slate-950` (Preto profundo/Azul escuro).
- [ ] **Imagem:** Imagem de alta resolução (`object-cover`) com `opacity-30`.
- [ ] **Overlay:** Gradiente `bg-gradient-to-t` (Slate-950 -> Transparent) para garantir legibilidade do texto inferior.
- [ ] **Partículas:** Elementos flutuantes (`bg-orange-500/20`) com animação suave de movimento aleatório.
#### 2.2. Elementos Centrais
- [ ] **Logo:** Componente `<Logo size="xl" />` centralizado no topo. Animação de entrada `fade-in` + `slide-down`.
- [ ] **Título:** Fonte `Inter`, Peso `Black` (900), Tamanho `text-7xl` (md: `text-9xl`).
    - Texto: "PEÇA" (Branco) + "AQUI" (Laranja `#ea580c`).
- [ ] **Subtítulo:** Texto `text-slate-300`, Uppercase, Tracking `wide`. "RÁPIDO • DIGITAL • SEM FILAS".
#### 2.3. Call to Action (CTA)
- [ ] **Botão:** Container branco (`bg-white`), bordas arredondadas extremas (`rounded-[3rem]`).
- [ ] **Sombra:** Glow laranja intenso (`shadow-[0_20px_50px_rgba(234,88,12,0.3)]`).
- [ ] **Animação:** `animate-pulse` ou escala suave (Zoom In/Out infinito).
- [ ] **Ícone:** `Touchpad` ou `HandClick` tamanho 48px, cor laranja.
- [ ] **Texto:** "TOQUE PARA COMEÇAR", Preto, Peso Black.
#### 2.4. Comportamento
- [ ] **Toque Global:** Clique em *qualquer* lugar da tela deve disparar a navegação.
- [ ] **Bloqueio:** Menu de contexto (botão direito) desabilitado. Seleção de texto desabilitada (`select-none`).
---
### 🔵 TELA 2: CARDÁPIO (Menu)
**Rota:** `/[slug]/menu?kiosk=true`
#### 2.5. Header (KioskHeader)
- [ ] **Fundo:** `bg-slate-900` sólido. Borda inferior `border-slate-800`.
- [ ] **Botão Voltar:** Gigante. `p-4`, `rounded-2xl`, `bg-slate-800`. Ícone `ArrowLeft` branco.
- [ ] **Identidade:** Logo da empresa + Nome. Badge "AUTOATENDIMENTO ATIVO" com `animate-ping` (ponto verde/laranja).
- [ ] **Instrução:** Card informativo à direita: "Toque nos itens para adicionar".
#### 2.6. Área de Produtos
- [ ] **Grid:** 2 colunas (Tablet Vertical) ou 3 colunas (Tablet Horizontal/Monitor).
- [ ] **Cards:**
    - Fundo: `bg-slate-900`.
    - Borda: `border-slate-800`.
    - Hover/Active: Borda muda para `border-orange-500/50`.
    - Imagem: Quadrada, `rounded-2xl`.
    - Preço: Fonte `text-xl`, Peso `Black`, Cor Primária da Empresa.
#### 2.7. Barra de Carrinho (Floating)
- [ ] **Posição:** Fixa no rodapé (`bottom-0`), largura total.
- [ ] **Botão:** Estilo "Pílula Gigante". Margem `p-6`.
- [ ] **Cor:** `bg-orange-600` (ou cor primária do tenant).
- [ ] **Conteúdo:**
    - Esquerda: Ícone `ShoppingBag` + Contador de Itens ("3 ITENS").
    - Centro/Direita: Total ("R$ 45,90") + Texto "FINALIZAR PEDIDO".
- [ ] **Animação:** `slide-in-from-bottom` quando o primeiro item é adicionado.
---
### 🟣 TELA 3: CHECKOUT
**Rota:** `/[slug]/checkout?kiosk=true`
#### 2.8. Layout Geral
- [ ] **Tema:** Dark Mode forçado (`bg-slate-950`, Texto Branco).
- [ ] **Cards:** `bg-slate-900`, `rounded-[2rem]`, `border-slate-800`.
#### 2.9. Etapa 1: Identificação
- [ ] **Input Nome:** Gigante (`p-4`, `text-lg`).
- [ ] **Teclado:** (Se não houver teclado físico) Input deve focar e abrir teclado virtual do OS ou componente de teclado virtual React (Backlog).
#### 2.10. Etapa 2: Pagamento
- [ ] **Grid de Métodos:** Botões grandes quadrados.
    - Ícone: 32px.
    - Label: Bold.
    - Estado Ativo: Borda Laranja + Fundo Laranja Translúcido (`bg-orange-500/10`).
#### 2.11. Etapa 3: Sucesso (Pós-Pagamento)
- [ ] **Ícone:** Check verde gigante (`w-32 h-32`) com animação de escala (`pop-in`).
- [ ] **Mensagem:** "Pedido Confirmado!".
- [ ] **Instrução:** "Aguarde a chamada pelo nome: [NOME]".
- [ ] **Feedback:** Texto piscante "Retornando à tela inicial em instantes...".
- [ ] **Ação:** Redirecionamento automático após 5s para `/kiosk`.
---
### 🔴 COMPORTAMENTOS DE SISTEMA (Invisíveis)
#### 2.12. Inactivity Timer
- [ ] **Gatilho:** 60 segundos sem toque na tela.
- [ ] **Modal:** "Ainda está aí?". Fundo `backdrop-blur`. Contador regressivo de 10s.
- [ ] **Ação de Timeout:** Limpar Carrinho (`clearCart()`) -> Redirecionar para `/kiosk`.
#### 2.13. Resiliência
- [ ] **Erro de Rede:** Toast vermelho no topo (Sonner). O app não deve travar.
- [ ] **Imagens Quebradas:** Fallback para ícone de `ImageIcon` cinza se a imagem do produto falhar.
---
*Checklist gerado para validação de Quality Assurance (QA) L6.*

