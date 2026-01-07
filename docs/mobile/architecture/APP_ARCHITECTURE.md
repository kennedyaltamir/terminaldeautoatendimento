# 🏗️ Arquitetura Interna do Aplicativo

## 1. Stack Tecnológica
- **Framework:** React Native com Expo (Managed Workflow).
- **Linguagem:** TypeScript (Strict Mode).
- **Estado Global:** Zustand (Leve e performático para mobile).
- **Server State:** React Query (Cache de API e sincronização).
- **Estilização:** NativeWind (Tailwind CSS para Native).

## 2. Camadas do Sistema
O padrão adotado é uma **Arquitetura em Camadas inspirada em Clean Architecture**, adaptada para o contexto pragmático de aplicações Mobile em React Native.

1.  **UI Layer (Screens/Components):** Componentes React puros e hooks de interface.
2.  **Domain Layer (Hooks/Logic):** Regras de negócio específicas do mobile (ex: cálculo de gorjeta).
3.  **Service Layer (API/Socket):** Clientes de comunicação externa.
4.  **Infrastructure Layer (Storage/Adapters):** Acesso a recursos nativos e persistência local.

## 3. Padrões de Navegação
*Nota: Decisão Arquitetural Antecipada (sem implementação nesta fase).*

- **React Navigation:** Estrutura de Stack para fluxos lineares e Tabs para navegação principal.
- **Deep Linking:** Suporte a abertura do app via QR Code de mesa ou links de rastreio.

## 4. Recomendação de Sequência
Sugere-se como próxima etapa a **Missão 11 — Infraestrutura de Autenticação Mobile (Auth, API Client, State)**, visando estabelecer uma base de segurança e comunicação sólida antes do desenvolvimento de interfaces.
