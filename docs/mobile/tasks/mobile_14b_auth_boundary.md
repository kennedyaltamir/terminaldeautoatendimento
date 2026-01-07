# 📱 Task 14B: Auth Boundary & Navigation Gate

## 1. Contexto
Criação da barreira de renderização soberana do aplicativo. O objetivo é garantir que a árvore de componentes operacional (`AppStack`) nunca seja montada sem um estado de sessão validado temporal e matematicamente.

## 2. Mapa de Renderização do AuthGate
| Status do Store | Renderização | Justificativa |
| :--- | :--- | :--- |
| `idle` | `null` | Aguardando início do JS. |
| `hydrating` | `null` | Lendo tokens do SecureStore. |
| `checking_expiry` | `null` | Validando validade do JWT. |
| `unauthenticated` | `<AuthStack />` | Sessão inexistente ou expirada. |
| `authenticated` | `<AppStack />` | Sessão válida e pronta. |

## 3. Decisões de Hardening
- **Exclusividade do RootNavigator:** O `RootNavigator` perdeu a função de decisor de telas. Sua única responsabilidade agora é disparar `hydrate()` no `useEffect` e renderizar o `AuthGate`.
- **Prevenção de Flicker:** O retorno de `null` em estados transitórios força o Sistema Operacional a manter o Splash Screen nativo visível, garantindo uma transição limpa para a tela de Login ou Home.

---
*Arquitetura de Navegação Mobile Encerrada — Janeiro de 2026*
