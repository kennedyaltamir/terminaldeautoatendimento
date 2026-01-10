# DOMAIN: OPERATIONS
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-OPS-02
TITLE: Real Transactional Email Service (SMTP)
OWNER: Executor Kernel
PRIORITY: ALTA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O `EmailService` atual (`app/services/email_service.py`) é um mock que apenas imprime o link de recuperação de senha no console do servidor.
- Em um ambiente de produção real ("Tudo Real"), os usuários finais não têm acesso ao console do servidor.
- A funcionalidade de "Esqueci minha senha" é inútil para usuários reais sem um envio de e-mail verdadeiro.
- O script de validação de integrações (`validate_integrations.py`) não verifica conectividade SMTP.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O `EmailService` utiliza o protocolo SMTP real para enviar e-mails transacionais.
- Suporte a provedores padrão de mercado (SendGrid, AWS SES, Gmail, Outlook) via configuração de ambiente.
- O template de ambiente de produção inclui variáveis SMTP.
- O script de validação testa a conexão com o servidor de e-mail.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Refatoração de `app/services/email_service.py` para usar `smtplib` e `email.mime`.
- Adição de variáveis SMTP em `.env.production.template`.
- Atualização de `scripts/production/validate_integrations.py` para incluir check de SMTP.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Templates HTML complexos (foco na entrega funcional do link).
- Filas de e-mail assíncronas (Celery) - envio será síncrono/background task simples por enquanto.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Protocolo: SMTP com STARTTLS ou SSL.
- Bibliotecas: Nativas do Python (`smtplib`, `email`).
- Segurança: Senhas lidas estritamente de variáveis de ambiente.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/services/email_service.py`
- `scripts/production/validate_integrations.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/services/email_service.py` (Real).
- `.env.production.template` (Atualizado).
- `scripts/production/validate_integrations.py` (Atualizado).

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] O serviço tenta conectar ao servidor SMTP configurado.
- [x] Se SMTP não estiver configurado, faz fallback gracioso para log (para não quebrar dev).
- [x] O script de validação reporta status da conexão SMTP.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/validate_integrations.py`
RESULTADO_ESPERADO: "SMTP: OK" ou "SMTP: WARN" (se não configurado), mas nunca crash.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/services/email_service.py` para versão mock.
