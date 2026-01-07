# 🎨 Plano Mestre de UX/UI: MesaFlow Fase 7

**Data:** 05 de Janeiro de 2026
**Status:** Aprovado para Execução
**Objetivo:** Elevar a percepção de valor do produto (Polimento Visual) e reduzir a fricção operacional (Usabilidade).

---

## 1. Autenticação & Onboarding
*A primeira impressão define a confiança no SaaS.*

### 1.1. Tela de Login (`/admin/login`)
- **Branding Fortalecido:**
    - *Ação:* Aumentar o logo "MesaFlow" e o ícone `ChefHat` (de `w-6` para `w-10`).
    - *Técnica:* Ajustar classes Tailwind no `Link` do header.
- **Visibilidade de Senha:**
    - *Ação:* Adicionar ícone `Eye/EyeOff` no input de senha.
    - *Técnica:* Estado local `showPassword` no componente `AuthInput`.
- **Feedback de Carregamento:**
    - *Ação:* Substituir o texto do botão por um `Loader2` girando durante a requisição.

### 1.2. Tela de Registro (`/admin/register`)
- **Input de Slug (Subdomínio):**
    - *Problema:* O usuário não entende que está criando um link.
    - *Solução:* Input Group. Prefixo fixo `mesaflow.com/` com fundo cinza (`bg-gray-100`) e o input real transparente ao lado.
- **Força da Senha:**
    - *Ação:* Barra de progresso colorida abaixo do input (Vermelho -> Amarelo -> Verde) baseada em Regex (Letras, Números, Símbolos).
- **Máscaras de Input:**
    - *Ação:* Formatar telefone automaticamente `(XX) XXXXX-XXXX` enquanto digita.
    - *Técnica:* Função utilitária `formatPhone` no `onChange`.

---

## 2. Dashboard & Analytics (`/admin/[slug]/dashboard`)
*Transformar dados frios em insights acionáveis.*

### 2.1. Cards de KPI
- **Indicadores de Tendência:**
    - *Ação:* Adicionar badge "⬆ 15%" (verde) ou "⬇ 5%" (vermelho) comparando com o período anterior.
    - *Técnica:* Calcular delta no backend ou no frontend (se tiver dados históricos).
- **Ícones Contextuais:**
    - *Ação:* Adicionar fundo translúcido colorido aos ícones (ex: `bg-green-100 text-green-600` para Faturamento).

### 2.2. Gráficos (Recharts)
- **Tooltips Ricos:**
    - *Ação:* Customizar o `Tooltip` do Recharts para mostrar "R$ 1.500,00" com formatação BRL e data completa, em vez de valores brutos.
- **Paleta de Cores:**
    - *Ação:* Garantir que as cores do gráfico sigam a identidade (Laranja Primário, Cinza Secundário) e não cores aleatórias.

---

## 3. Gestão de Cardápio (`/admin/[slug]/menu`)
*A área mais usada pelo gestor precisa ser fluida.*

### 3.1. Organização Visual
- **Accordion (Colapso):**
    - *Ação:* Permitir clicar no cabeçalho da Categoria para esconder/mostrar os produtos. Útil para cardápios grandes.
    - *Técnica:* Estado local `expandedCategories: number[]`.
- **Drag & Drop:**
    - *Ação:* Ícone de "Grip" (seis pontos) ao lado dos produtos para reordenar.
    - *Técnica:* Biblioteca `dnd-kit` ou `react-beautiful-dnd` (Implementação futura, preparar UI agora).

### 3.2. Busca Interna
- **Filtro Rápido:**
    - *Ação:* Input de busca no topo da lista de produtos que filtra em tempo real (client-side) por nome.

---

## 4. Estoque (`/admin/[slug]/inventory`)
*Prevenção de erros operacionais.*

### 4.1. Alertas Visuais
- **Linhas de Perigo:**
    - *Ação:* Se `current_stock <= min_stock_alert`, a linha da tabela ganha fundo vermelho claro (`bg-red-50`) e texto vermelho.
- **Edição Inline:**
    - *Ação:* Ao clicar na quantidade, transforma em input numérico para ajuste rápido (Inventário relâmpago).

---

## 5. Configurações (`/admin/[slug]/settings`)
*Reduzir a complexidade cognitiva de formulários longos.*

### 5.1. Navegação
- **Sticky Sidebar:**
    - *Ação:* Manter o menu lateral de abas fixo enquanto a página rola.
    - *Técnica:* `sticky top-4` no container das abas.

### 5.2. Segurança de Tokens
- **Mascaramento:**
    - *Ação:* Inputs de Token (WhatsApp, MP, Fiscal) devem ser `type="password"` por padrão, com botão "Revelar".

### 5.3. Feedback de Conexão
- **Botão de Teste:**
    - *Ação:* Ao lado da config de WhatsApp, botão "Enviar Teste" que dispara uma mensagem real para o número do dono.

---

## 6. KDS - Cozinha (`/admin/[slug]/kitchen`)
*Interface para ambientes caóticos e engordurados.*

### 6.1. Acessibilidade de Toque
- **Botões Gigantes:**
    - *Ação:* Aumentar `padding` e `min-height` dos botões de ação ("Iniciar", "Pronto"). Alvos de toque devem ter no mínimo 48px.
- **Filtros de Estação:**
    - *Ação:* Transformar os links de texto em botões grandes estilo "Pílula" (`rounded-full`).

### 6.2. Imersão
- **Modo Tela Cheia:**
    - *Ação:* Botão que aciona `document.documentElement.requestFullscreen()`. Remove a barra de endereços do navegador.

---

## 7. Cardápio Público (`/[slug]/menu`)
*Conversão e facilidade de compra.*

### 7.1. Navegação Sticky
- **Barra de Categorias:**
    - *Ação:* A barra de categorias deve grudar no topo (`sticky top-0`) logo abaixo do header quando rolar a página.
    - *Técnica:* Ajuste de `z-index` e `top`.

### 7.2. Adição Rápida (Quick Add)
- **Botão Inteligente:**
    - *Lógica:* Se o produto NÃO tem opcionais obrigatórios, o botão "+" adiciona direto ao carrinho (com animação de voo para o ícone da sacola).
    - *Lógica:* Se TEM opcionais, abre o modal.

### 7.3. Botão "Voltar ao Topo"
- **Usabilidade:**
    - *Ação:* Botão flutuante discreto que aparece após rolar 2 telas, permitindo voltar ao início rapidamente.

---

## 8. App do Garçom (`/admin/[slug]/waiter`)
*Agilidade no salão.*

### 8.1. Pull to Refresh
- **Atualização:**
    - *Ação:* Implementar gesto de puxar para baixo para recarregar o status das mesas (além do WebSocket).

### 8.2. Skeleton Loading
- **Percepção de Performance:**
    - *Ação:* Substituir o texto "Carregando..." por esqueletos pulsantes (`animate-pulse`) que imitam o layout dos cards de mesa.

---

## Prioridade de Execução

1.  **Grupo A (Conversão & Identidade):** Login, Registro, Cardápio Público.
2.  **Grupo B (Operação Crítica):** KDS, App Garçom.
3.  **Grupo C (Gestão):** Dashboard, Estoque, Configurações.
