# 🚀 Guia de Deploy MesaFlow (Nuvem PaaS)

Este documento detalha como configurar os serviços de produção usando a arquitetura atual.

## 🏢 1. Backend & API (Render.com)
1. **Service Type:** Web Service.
2. **Build Command:** `pip install -r requirements.txt`.
3. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. **Health Check Path:** `/api/health` (Crucial para monitoramento).
5. **Environment Variables:**
   - `DATABASE_URL`: Pegue no painel do Neon.tech (Modo Pooled recomendado).
   - `REDIS_URL`: URL do Render Redis ou Upstash.
   - `SECRET_KEY`: Gere uma chave aleatória forte.
   - `ENVIRONMENT`: `production`.

## 🗄️ 2. Banco de Dados (Neon.tech)
1. Utilize a string de conexão que termina com `-pooler`. Isso garante que o Render consiga manter muitas conexões simultâneas sem estourar o limite do Postgres.

## 🎨 3. Frontend (Vercel.com)
1. **Framework Preset:** Next.js.
2. **Root Directory:** `frontend`.
3. **Build Command:** `npm run build`.
4. **Environment Variables:**
   - `NEXT_PUBLIC_API_URL`: `https://sua-api.onrender.com/api`.
   - `NEXT_PUBLIC_WS_URL`: `wss://sua-api.onrender.com/ws`.

## 📡 4. WebSockets na Nuvem
O Render suporta WebSockets nativamente. Certifique-se de que o frontend usa o protocolo `wss://` (seguro) para evitar erros de Mixed Content.

---
*Manual atualizado para MesaFlow v2.3.1*
# 🚀 Guia de Deploy MesaFlow (Nuvem PaaS)

Este documento detalha como configurar e manter os serviços de produção.

## 🏢 1. Backend & API (Render.com)

### ⚙️ Configurações Iniciais:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/api/health`

### 🔄 Procedimento de Atualização Limpa:
Sempre que houver mudanças em dependências (`requirements.txt`) ou variáveis de ambiente críticas:
1. Vá ao painel do serviço no Render.
2. Clique em **Manual Deploy**.
3. Selecione **Clear build cache & deploy**.
4. Acompanhe a aba **Logs** até visualizar a mensagem de sucesso e o status **Live**.

## 🗄️ 2. Banco de Dados (Neon.tech)
- Utilize sempre o **Connection Pooling** para evitar que o limite de conexões do Postgres seja atingido pelo Render.
- A string de conexão deve terminar com `?sslmode=require`.

## 🎨 3. Frontend (Vercel.com)
- Deploys são automáticos ao fazer `git push` para a branch `main`.
- Certifique-se de que a variável `NEXT_PUBLIC_API_URL` aponta para o link `.onrender.com` correto.

---
*Manual atualizado para MesaFlow v2.3.1 - Janeiro 2026*
