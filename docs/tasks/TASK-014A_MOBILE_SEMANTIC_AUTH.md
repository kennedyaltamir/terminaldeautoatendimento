# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-014A
TITLE: Implementar Validação Semântica e Temporal de JWT no Mobile
OWNER: Executor Kernel
PRIORITY: CRÍTICA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O aplicativo mobile utiliza `SecureStore` para persistir tokens.
- O estado de autenticação (`authenticated`) é determinado apenas pela existência física das chaves `mesaflow_access_token` e `mesaflow_refresh_token`.
- Não existe validação do campo `exp` (expiration) do JWT no lado do cliente.
- Não existe validação das claims obrigatórias (`company_id`, `role`) no lado do cliente.
- O arquivo `mobile/src/services/auth/jwt.ts` contém apenas um esqueleto ou lógica básica.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O `AuthStore` executa uma verificação matemática no payload do JWT durante a hidratação.
- O sistema considera o token inválido se `now() > exp - 10s` (Buffer de segurança).
- O sistema considera o token inválido se as claims `sub`, `role` ou `company_id` estiverem ausentes.
- O estado global transita automaticamente para `unauthenticated` se a validação falhar, forçando um novo login ou refresh.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Implementação de `JwtService.validateClaims(token)` em `mobile/src/services/auth/jwt.ts`.
- Implementação de `JwtService.isTokenExpired(token)` com buffer de 10s.
- Atualização do método `hydrate()` em `mobile/src/store/auth.store.ts` para usar essas validações.
- Instalação da dependência `jwt-decode` (se ainda não estiver instalada/configurada corretamente).

### EXCLUI
- Criação de telas de UI (Login, Home).
- Alterações no Backend (API).
- Alterações no fluxo de Refresh Token (apenas a validação inicial é o foco).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Linguagem: TypeScript (Strict Mode).
- Frameworks permitidos: `jwt-decode` (ou `base-64` se necessário para polyfill).
- Alterar arquitetura: NÃO.
- Criar novos serviços: NÃO (Apenas atualizar `jwt.ts`).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Código fonte atual em `mobile/src/store/auth.store.ts`.
- Código fonte atual em `mobile/src/services/auth/jwt.ts`.
- Biblioteca `core-js` ou `base-64` para decode se o ambiente Hermes exigir.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivo `mobile/src/services/auth/jwt.ts` atualizado.
- Arquivo `mobile/src/store/auth.store.ts` atualizado.
- Arquivo `mobile/package.json` atualizado (se houver nova dependência).

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] `JwtService.isTokenExpired` retorna `true` para token vencido.
- [ ] `JwtService.validateClaims` retorna `false` para token sem `company_id`.
- [ ] `AuthStore.hydrate` define status como `unauthenticated` se o token for inválido, mesmo que exista no storage.
- [ ] O código compila sem erros de TypeScript.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `npm test mobile/src/store/__tests__/auth.store.test.ts`
RESULTADO_ESPERADO: Todos os testes passando (Green), incluindo novos casos de teste para token inválido.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `mobile/src/store/auth.store.ts` para a versão anterior (confiança cega no storage).
- Reverter `mobile/src/services/auth/jwt.ts`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO adicionar lógica de redirecionamento de navegação dentro do Store (deve ser reativo via AuthGate).
- É PROIBIDO fazer chamadas de API (`fetch` / `axios`) dentro do `JwtService` (deve ser uma função pura).
