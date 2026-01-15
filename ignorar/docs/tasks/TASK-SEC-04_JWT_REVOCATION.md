# DOMAIN: SECURITY
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-SEC-04
TITLE: JWT Token Revocation & Redis-based Blocklist
OWNER: Executor Kernel
PRIORITY: ALTA (ENTERPRISE / SECURITY)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema utiliza autenticação baseada em JWT (Stateless).
- Uma vez emitido, um token de acesso é válido até sua expiração (30 min), sem possibilidade de revogação centralizada.
- Em caso de comprometimento de credenciais ou perda de dispositivo, o atacante mantém acesso até o fim da validade do token.
- Auditorias Enterprise exigem um mecanismo de "Kill Switch" para invalidar sessões ativas (Force Logout).

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de uma camada de revogação de tokens utilizando o Redis como armazenamento de alta performance para a "Blacklist".
- Inclusão de um identificador único (`jti`) em cada JWT emitido.
- Middleware de segurança validando a presença do `jti` na blacklist em tempo real.
- Endpoint de Logout que invalida permanentemente o token utilizado.
- Suporte a "Logout Global" (invalidação de todas as sessões de um usuário/empresa).

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Atualização do serviço de segurança em `app/core/security.py` para incluir `jti`.
- Criação de `app/services/token_service.py` para interface com Redis.
- Atualização do middleware de dependência `get_current_user` em `app/routers/auth.py`.
- Adição da rota `POST /api/auth/logout`.
- Script de validação de revogação.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Persistência de tokens revogados em banco de dados relacional (uso exclusivo do Redis/Cache).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Latência: A verificação no Redis deve adicionar < 5ms à requisição.
- Persistência: Tokens revogados devem expirar no Redis automaticamente após o tempo original de vida do JWT.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/core/security.py`
- `app/routers/auth.py`
- `app/websockets.py` (Referência de uso de Redis)

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/core/security.py` (Atualizado).
- `app/services/token_service.py` (Novo).
- `app/routers/auth.py` (Atualizado).
- `scripts/production/verify_jwt_revocation.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Novos tokens emitidos contêm a claim `jti`.
- [x] O endpoint `/logout` adiciona o `jti` ao Redis.
- [x] Requisições subsequentes com o mesmo token são rejeitadas com 401 Unauthorized.
- [x] O script de validação confirma o bloqueio do token após o logout.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_jwt_revocation.py`
RESULTADO_ESPERADO: "JWT Revocation Verified: Token blocked after logout."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter lógica de `get_current_user` para ignorar o check de blacklist.
