# DOMAIN: SECURITY
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-07
TITLE: Enterprise Security Polish (CSP Strict + Governance)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O middleware de segurança implementa headers básicos, mas o CSP (`default-src 'self'`) é considerado permissivo para padrões SOC2/ISO 27001.
- O header HSTS carece da diretiva `preload`, impedindo a pontuação máxima em scanners de segurança.
- Existe execução de testes de segurança, mas falta a formalização da Governança de Segurança (`SECURITY_POLICY.md`) definindo SLAs e responsabilidades.
- O pipeline de CI/CD não menciona explicitamente a execução do pentest automatizado.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- API servindo headers CSP estritos (`object-src 'none'`, `base-uri 'self'`, etc.).
- HSTS configurado com `preload` para inclusão na lista de pré-carregamento dos navegadores.
- Documento `docs/security/SECURITY_POLICY.md` criado e formalizado.
- Script de pentest atualizado para validar as novas regras estritas.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Endurecimento do Middleware em `app/main.py`.
- Criação da Política de Segurança Institucional.
- Atualização do script de auditoria `scripts/security/automated_pentest.py` para critérios Enterprise.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Submissão real do domínio para a lista HSTS Preload (apenas a configuração técnica).
- Auditoria externa.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Padrão: OWASP Secure Headers (Nível Paranoico/Enterprise).
- Formato: Markdown para documentação.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/main.py`
- `scripts/security/automated_pentest.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/main.py` (Hardened).
- `docs/security/SECURITY_POLICY.md` (Novo).
- `scripts/security/automated_pentest.py` (Atualizado).

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] CSP inclui `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`.
- [x] HSTS inclui `preload`.
- [x] Política de Segurança define SLA de correção de vulnerabilidades.
- [x] Script de pentest valida especificamente as novas diretivas.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/security/automated_pentest.py`
RESULTADO_ESPERADO: "SECURITY AUDIT PASSED: Enterprise Grade Headers Verified."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/main.py`.
- Remover `docs/security/SECURITY_POLICY.md`.