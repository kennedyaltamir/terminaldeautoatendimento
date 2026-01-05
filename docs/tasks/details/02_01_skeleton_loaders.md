# 🎨 Detalhamento Técnico: Skeleton Loaders (UX-01)

## 1. Visão Geral
Implementação de telas de carregamento progressivo para eliminar o *Cumulative Layout Shift* (CLS) e melhorar a percepção de performance do usuário final.

## 2. Especificação Técnica
### 2.1 Componente Base (`Skeleton.tsx`)
- **Tecnologia:** Tailwind CSS + React.
- **Estilo:** Fundo cinza neutro (`bg-gray-200`) com animação de opacidade (`animate-pulse`).
- **Flexibilidade:** Deve aceitar propriedades de `width`, `height` e `borderRadius` para se adaptar a qualquer layout.

### 2.2 Componente de Negócio (`MenuSkeleton.tsx`)
- **Estrutura:** Deve replicar visualmente:
    - 1 Header (Logo + Nome).
    - 1 Barra de Busca.
    - 1 Navegação de Categorias (Pílulas).
    - 3 Seções de Categoria, cada uma com 2-3 cards de produtos.
- **Objetivo:** Manter o scroll estável enquanto os dados reais preenchem os espaços.

## 3. Fluxo de Implementação
1.  **Criação do Átomo:** Desenvolver o componente `Skeleton` genérico.
2.  **Composição do Layout:** Montar o `MenuSkeleton` usando os átomos.
3.  **Injeção de Estado:** No `MenuClient.tsx`, substituir o retorno de "Carregando..." pelo `<MenuSkeleton />`.
4.  **Refinamento de Tema:** Garantir que as cores do skeleton se adaptem ao Dark Mode.

## 4. Testes e Validação
- **Visual:** Verificar se não há "pulos" de layout quando o `loading` muda para `false`.
- **Performance:** Medir o *First Contentful Paint* (FCP) via Lighthouse.
- **Automatizado:** Teste Playwright validando a presença da classe `animate-pulse` no carregamento inicial.
