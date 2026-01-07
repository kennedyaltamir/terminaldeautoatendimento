# 🎨 Design System Mobile: MesaFlow

## 1. Filosofia Visual
O MesaFlow Mobile adota uma estética **Dark-First**, priorizando alto contraste, legibilidade em ambientes de baixa luz (cozinhas/bares) e foco em ações rápidas.

## 2. Tokens de Cor
| Nome | Hex | Uso |
| :--- | :--- | :--- |
| **Primary** | `#EA580C` | Ações principais, botões, destaques. |
| **Background** | `#0F172A` | Fundo principal das telas. |
| **Surface** | `#1E293B` | Cards, modais, inputs. |
| **Text-Primary** | `#FFFFFF` | Títulos e textos de leitura. |
| **Text-Secondary** | `#94A3B8` | Legendas e textos auxiliares. |
| **Error** | `#EF4444` | Alertas e ações destrutivas. |

## 3. Tipografia
- **H1:** 32px, Bold, Tracking Tight.
- **H2:** 24px, Bold.
- **Body:** 16px, Regular.
- **Caption:** 12px, Medium, Uppercase.

**Nota:** O uso de `fontFamily: 'System'` é uma decisão provisória para garantir compatibilidade imediata. O sistema está preparado para substituição por fontes customizadas sem alteração na API dos componentes.

## 4. Componentes Base
- **Typography:** Wrapper para o componente `Text` nativo com variantes semânticas.
- **Button:** Componente de ação. Utiliza `TouchableOpacity` por design para garantir feedback visual consistente em todas as plataformas.
- **Input:** Campo de texto com suporte a ícones e estados de erro.
- **Card:** Superfície base para agrupamento de conteúdo.
- **Layout Helpers:** Componentes `Stack`, `Spacer` e `Container` para gestão de fluxo espacial.

## 5. Limitações e Escopo Atual
Nesta fase (v1.0), o Design System **NÃO** contempla:
- Tokens semânticos de sombra (utiliza-se elevação padrão ou bordas).
- Tokens de grid complexos (utiliza-se o sistema de `Stack`).
- Animações complexas de transição de estado.

---
*Versão 1.1 — Janeiro de 2026*
