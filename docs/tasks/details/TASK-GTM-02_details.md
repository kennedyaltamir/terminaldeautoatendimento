# 👁️ Detalhamento Técnico: Observabilidade Fullstack (TASK-GTM-02)

## 1. Contexto
Atualmente, erros em produção dependem de relatos de usuários ou logs efêmeros do console. Precisamos de rastreamento proativo de exceções e performance.

## 2. Especificação de Implementação

### 2.1 Backend (Sentry Python)
- **Inicialização:** No `app/main.py`, antes de criar o `FastAPI()`.
- **Contexto:** Middleware que injeta `company_id` no escopo do Sentry assim que o JWT é validado.
- **Sanitização:** `before_send` deve remover corpos de requisição que contenham senhas ou dados de cartão.
- **Performance:** `traces_sample_rate=0.1` (10% das requisições) para evitar custos excessivos, mas `1.0` para erros.

### 2.2 Frontend (Sentry Next.js)
- **Configuração:** `sentry.client.config.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`.
- **Replay:** Ativar `replaysOnErrorSampleRate: 1.0`. Isso grava um vídeo de 30s do que o usuário fez antes do crash.
- **Source Maps:** Configurar o upload de source maps no build para desofuscar o código no painel do Sentry.

### 2.3 Logs Estruturados (JSON)
Substituir `print()` por um logger configurado.
- **Formato:**
  ```json
  {
    "timestamp": "2026-01-08T10:00:00Z",
    "level": "INFO",
    "service": "backend",
    "module": "payment_service",
    "message": "Pagamento processado",
    "company_id": "uuid...",
    "order_id": "uuid..."
  }
  ```
- **Benefício:** Permite filtros avançados em ferramentas de log (Datadog, CloudWatch, Render Logs).

## 3. Plano de Validação
1.  Criar rota oculta `/api/debug/crash` que levanta `RuntimeError`.
2.  Acessar a rota e verificar se o erro aparece no Sentry com o `company_id` correto.
3.  Verificar se os logs no terminal estão em JSON.
