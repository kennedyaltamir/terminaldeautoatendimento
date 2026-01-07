# 📱 Arquitetura Mobile Nativa: MesaFlow v1.0

## 1. Visão Geral
O aplicativo móvel do MesaFlow é projetado para oferecer a melhor experiência operacional para Garçons, Cozinheiros e Entregadores, utilizando tecnologias nativas para garantir performance, acesso a hardware (impressoras, vibração) e notificações em tempo real.

## 2. Stack Tecnológica
- **Framework:** React Native com Expo (Managed Workflow).
- **Linguagem:** TypeScript (Strict Mode).
- **Estilização:** NativeWind (Tailwind CSS para React Native).
- **Gerenciamento de Estado:** Zustand (Global) e React Query (Server State).
- **Navegação:** React Navigation (Stack & Tabs).
- **Segurança:** Expo SecureStore para persistência de tokens JWT.
- **Ícones:** Lucide React Native.

## 3. Estrutura de Pastas
```text
mobile/
├── src/
│   ├── api/            # Axios instances e chamadas de API
│   ├── components/     # Componentes atômicos e moleculares
│   ├── hooks/          # Hooks customizados (auth, socket, etc)
│   ├── navigation/     # Configuração de rotas e guards
│   ├── screens/        # Telas principais do app
│   ├── store/          # Zustand stores (auth, settings)
│   ├── theme/          # Configurações de cores e constantes
│   └── utils/          # Funções utilitárias e formatadores
├── __tests__/          # Testes unitários e de integração
├── app.json            # Configuração do Expo
└── package.json
```

## 4. Fluxo de Autenticação
O app mobile consome os mesmos endpoints de `/api/auth/token` e `/api/auth/refresh` do ecossistema web.
1. **Login:** O usuário insere credenciais; o app recebe `access_token` e `refresh_token`.
2. **Persistência:** Os tokens são salvos no `SecureStore`.
3. **Interceptor:** Um interceptor do Axios anexa o Bearer token em cada requisição.
4. **Refresh:** Caso receba um erro 401, o app tenta renovar o token automaticamente antes de deslogar o usuário.

## 5. Estratégia de Testes
- **Unitários:** Testar lógica de formatadores, stores do Zustand e hooks.
- **Componentes:** Validar renderização e interações básicas com React Testing Library.
- **Integração:** Mockar chamadas de API (MSW ou Jest Mocks) para validar fluxos de login e listagem.

---
*Versão 1.0 - Janeiro de 2026*
