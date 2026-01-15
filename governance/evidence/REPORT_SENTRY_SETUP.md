
# 👁️ Guia de Configuração: Sentry (Observabilidade)

**Status:** BLOQUEANTE (OBS-01 FAILED)
**Objetivo:** Habilitar a telemetria de erros para desbloquear o Go-Live.

---

## 1. Por que isso é obrigatório?
Sem o Sentry, o sistema roda "às cegas". Se um erro 500 ocorrer em produção, não haverá log centralizado, stack trace ou contexto do usuário. O Protocolo INDA L6 proíbe deploys sem observabilidade.

## 2. Passo a Passo de Configuração

### Passo A: Criar Conta/Projeto
1. Acesse [sentry.io](https://sentry.io).
2. Crie uma conta (Plano Developer é gratuito e suficiente).
3. Crie um novo projeto:
   - **Plataforma:** Python (FastAPI)
   - **Nome:** `mesaflow-backend`

### Passo B: Obter o DSN (Data Source Name)
1. No projeto criado, vá em **Settings** > **Client Keys (DSN)**.
2. Copie o valor do DSN. Ele se parece com:
   `https://exemploPublicKey@o0.ingest.sentry.io/0`

### Passo C: Configurar o Ambiente
1. Abra o arquivo `.env` na raiz do projeto.
2. Localize ou adicione a chave `SENTRY_DSN_BACKEND`.
3. Cole o valor obtido.

```ini
# .env
SENTRY_DSN_BACKEND=https://seu_dsn_real_aqui@o0.ingest.sentry.io/0
```

### Passo D: Validar
1. Execute o script de teste de ingestão:
   ```bash
   python comunication/scripts/sentry_ingest_test.py
   ```
2. Se o script retornar `✅ Sentry Ingest Test Passed`, o bloqueio foi removido.

---

## 3. Próximos Passos (Pós-Desbloqueio)
Após configurar o `.env`, execute novamente o ciclo de validação para atualizar o `registry.xml` para `SUCCESS`.

*MesaFlow Kernel L6*

