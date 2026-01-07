# 📱 Task 12: Camada de Aplicação e Estado Global

## 1. Contexto
Após a consolidação da infraestrutura de rede (Missão 11), esta missão implementa o gerenciamento de estado global de autenticação, servindo como a ponte lógica para a futura interface de usuário.

## 2. Lifecycle da Sessão
O estado de autenticação segue um fluxo determinístico:

1. **Cold Start:** O App é aberto. O estado inicial é `idle`.
2. **Hydration:** A action `hydrate()` é disparada. O status muda para `hydrating`.
3. **Resolution:** 
   - Se tokens existem no `SecureStore` -> `authenticated`.
   - Se tokens ausentes -> `unauthenticated`.
4. **Runtime:** O estado permanece em `authenticated` enquanto o interceptor de refresh (Infra) mantiver a validade dos tokens.
5. **Termination:** O `logout()` limpa o storage e reseta o estado para `unauthenticated`.

## 3. Contratos de Estado
- **Status:** `idle` | `hydrating` | `authenticated` | `unauthenticated` | `error`.
- **User:** Objeto tipado contendo perfil e vínculo multi-tenant.
- **Error:** Objeto contendo `AuthErrorType` para tratamento semântico na UI.

## 4. Limites da Missão
- **UI:** Nenhuma interface visual foi criada.
- **Navegação:** Nenhuma rota ou navigator foi configurado.
- **Infra:** Nenhuma alteração foi feita nos serviços de rede.

## 5. Validação Semântica de Sessão (Dívida Técnica Conhecida)
Nesta missão, o estado `authenticated` é determinado exclusivamente pela presença de tokens válidos no `SecureStore`. 

A validação semântica do token (ex: `exp`, `iat`, claims, escopo, ou sincronização com endpoint `/me`) **não faz parte do escopo da Missão 12**. Esta validação será implementada em missão futura dedicada, responsável pelo bootstrap completo da sessão, autorização por papel e consistência entre estado local e backend.

---
*Ajuste Documental de Governança — Janeiro de 2026*
