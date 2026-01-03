# 🎨 Arquitetura do Frontend (MesaFlow Client)

Este documento descreve a estrutura do cliente web desenvolvido em **Next.js 14 (App Router)** com **Tailwind CSS**.

## 1. Visão Geral
O frontend é uma aplicação SPA (Single Page Application) otimizada para mobile. Ele consome a API REST do MesaFlow e possui dois contextos distintos:
1.  **Menu Público:** Onde o cliente final faz o pedido.
2.  **KDS (Kitchen Display System):** Onde a cozinha visualiza os pedidos.

## 2. Estrutura de Pastas (Next.js App Router)

```text
src/
├── app/
│   ├── layout.tsx           # Layout global (Fontes, Metadados)
│   ├── page.tsx             # Landing Page (Home do SaaS)
│   │
│   ├── [slug]/              # Rota Dinâmica (ex: /hamburgueria-ze)
│   │   └── menu/
│   │       └── page.tsx     # O Cardápio Digital (Principal)
│   │
│   └── admin/
│       └── kitchen/
│           └── page.tsx     # Tela da Cozinha (KDS)
│
├── components/              # Componentes Reutilizáveis
│   ├── ui/                  # Botões, Cards, Modais (Burros/Visuais)
│   ├── menu/                # Lógica específica do menu (ProductCard, CategoryList)
│   └── cart/                # Carrinho de compras flutuante
│
├── context/
│   └── CartContext.tsx      # Gerenciamento de Estado Global (Carrinho)
│
├── lib/
│   └── api.ts               # Cliente HTTP (Fetch wrappers)
│
└── types/
    └── index.ts             # Tipagem TypeScript (Espelho dos Schemas Pydantic)