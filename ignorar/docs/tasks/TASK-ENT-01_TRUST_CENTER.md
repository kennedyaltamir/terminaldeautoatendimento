# DOMAIN: FRONTEND
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-ENT-01
TITLE: Trust Center Público (Status Page + Security Disclosure)
OWNER: Executor Kernel
PRIORITY: ALTA (ENTERPRISE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema possui controles de segurança robustos (CSP, HSTS, RLS), mas essas informações estão ocultas em documentação técnica interna ou headers HTTP.
- Não existe uma página pública unificada onde clientes Enterprise possam verificar a saúde do sistema ou as políticas de segurança durante processos de due diligence.
- A ausência de um "Trust Center" gera fricção comercial, exigindo envio manual de documentos.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação da rota `/trust` (Trust Center) no Frontend.
- Página `/trust/status`: Exibe o estado operacional dos serviços (API, Database, Redis) consumindo o endpoint de health check.
- Página `/trust/security`: Exibe publicamente as políticas de segurança, conformidade (LGPD) e canal de denúncia.
- Layout profissional e sóbrio, focado em transparência.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Layout específico para a área de Trust (`frontend/src/app/trust/layout.tsx`).
- Página Index (`frontend/src/app/trust/page.tsx`).
- Página de Status (`frontend/src/app/trust/status/page.tsx`) com verificação live.
- Página de Segurança (`frontend/src/app/trust/security/page.tsx`).
- Script de validação de rotas.

### EXCLUI
- Integração com ferramentas de terceiros (Statuspage.io, Atlassian).
- Dashboard de métricas históricas de uptime (apenas estado atual).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: Next.js 14 (App Router).
- Estilização: Tailwind CSS.
- Acesso: Público (Sem autenticação).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Endpoint `/api/health` (já existente).
- Conteúdo de `SECURITY.md` e `PRIVACY_POLICY.md`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivos de rota Next.js.
- Script `scripts/production/verify_trust_center.py`.
- Atualização do `docs/TASKS.md`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Rota `/trust` acessível publicamente.
- [x] Página de Status consulta `/api/health` e exibe resultado visual.
- [x] Página de Segurança lista controles (RLS, Criptografia) e contatos.
- [x] Script de validação retorna sucesso (200 OK nas rotas).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_trust_center.py`
RESULTADO_ESPERADO: "Trust Center Verification Passed: All routes active."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover diretório `frontend/src/app/trust`.