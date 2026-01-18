# 🎨 Especificação Técnica: TASK-UX-02
> **Título:** Redesign Moderno e "Smooth" (Landing & Admin)
> **Status:** SPECIFIED

## 1. Visão Estética
O objetivo é transitar de uma interface "funcional/técnica" para uma experiência "Premium/SaaS".
- **Estilo:** Glassmorphism sutil, bordas arredondadas (24px+), sombras suaves e profundidade.
- **Movimento:** Transições de página via Framer Motion (fade e slide), micro-interações em botões (scale 0.95).
- **Tipografia:** Substituição por "Plus Jakarta Sans" ou "Inter" com kerning ajustado.

## 2. Componentes Alvo
### 2.1. Landing Page
- Hero section com gradientes animados.
- Cards de recursos com efeito de hover magnético.
- Prova social com logos em grayscale que ganham cor no hover.

### 2.2. Painel Admin
- Sidebar colapsável com ícones minimalistas.
- Dashboards com widgets flutuantes.
- Tabelas com zebra-striping suave e ações rápidas no hover.

## 3. Requisitos Técnicos
- Implementação de `framer-motion` em componentes core.
- Uso de `shadcn/ui` para componentes de base (Select, Popover, Command).
- Garantia de contraste WCAG AA.
