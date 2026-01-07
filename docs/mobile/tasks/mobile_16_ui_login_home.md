# 📱 Task 16: UI Real — Login & Home

## 1. Objetivo da Missão
Transição da infraestrutura mobile para a interface funcional real. Implementação das telas de Login e Home utilizando o Design System técnico (Tokens + UI Foundation).

## 2. Estrutura das Telas
- **LoginScreen**: Containerizado em um `Card`, com inputs para e-mail e senha. Foco em centralização e feedback de estado (loading/error).
- **HomeScreen**: Exibe dados de confirmação de sessão (E-mail e Role) e permite o encerramento da sessão (Logout).

## 3. Conexão com Auth Store
A UI reage aos estados semânticos da `useAuthStore`:
- **Estado 'hydrating'**: Utilizado para desabilitar inputs e ativar o spinner no `Button` durante a chamada de login.
- **Estado 'error'**: O componente `Input` de senha exibe a mensagem de erro retornada pelo backend/store.
- **Action 'logout'**: Limpa o `SecureStore`, movendo o status para `unauthenticated`, o que faz o `AuthGate` trocar as Stacks de navegação automaticamente.

## 4. O que NÃO foi implementado (Out of Scope)
- Validação complexa de formulário no client (Zod/Hook Form).
- Lógica de autorização baseada em cargos (ex: ocultar botões se for `driver`).
- Estilização de avatar ou dashboard de dados.

## 5. Próximo Passo Sugerido
Início da Missão 17 — Módulo de Pedidos (KDS Nativo), consumindo os endpoints operacionais do backend para listar e gerenciar o fluxo de produção diretamente do app.

---
*Fase 10 — Janeiro de 2026*
