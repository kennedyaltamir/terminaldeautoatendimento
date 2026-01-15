# DOMAIN: SECURITY
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-06
TITLE: Security Hardening & Automated Pentest (Blindagem Enterprise)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema possui autenticação JWT e RLS (Row-Level Security) no banco de dados.
- A API não impõe cabeçalhos de segurança HTTP estritos (HSTS, CSP, X-Frame-Options) de forma centralizada.
- Não existe um mecanismo automatizado de "Pentest Contínuo" para validar a postura de segurança antes de cada deploy.
- A ausência desses controles impede a aprovação em auditorias de segurança corporativas (SOC2 / ISO 27001).

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Middleware de Segurança (`SecurityHeadersMiddleware`) implementado no FastAPI, forçando headers de proteção em todas as respostas.
- Script de Pentest Automatizado (`scripts/security/automated_pentest.py`) capaz de verificar:
    - Presença de Headers de Segurança.
    - Resiliência contra XSS básico.
    - Bloqueio de Path Traversal.
    - Proteção de rotas administrativas.
- Sistema aprovado com nota "A" em simuladores de segurança de headers.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Implementação de Middleware em `app/main.py`.
- Configuração de HSTS (Strict-Transport-Security), CSP (Content-Security-Policy), X-Content-Type-Options, Referrer-Policy.
- Criação do script de auditoria `scripts/security/automated_pentest.py`.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Implementação de WAF (Web Application Firewall) externo (Cloudflare/AWS).
- Testes de DDoS volumétrico.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: FastAPI (Middleware).
- Linguagem: Python 3.11+.
- Padrão: OWASP Secure Headers Project.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/main.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/main.py` (Atualizado com Middleware).
- `scripts/security/automated_pentest.py` (Novo).
- `docs/TASKS.md` (Atualizado).

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Todas as respostas da API contêm o header `Strict-Transport-Security`.
- [x] Todas as respostas contêm `X-Content-Type-Options: nosniff`.
- [x] O script de pentest executa com Exit Code 0.
- [x] Tentativas de injeção básica são sanitizadas ou rejeitadas.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/security/automated_pentest.py`
RESULTADO_ESPERADO: "SECURITY AUDIT PASSED: All checks green."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover o middleware de segurança de `app/main.py`.
- Excluir o script de pentest.