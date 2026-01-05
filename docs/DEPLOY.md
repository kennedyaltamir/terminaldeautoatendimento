
---

### 4️⃣ `docs/DEPLOY.md` (Pragmático)

Passo a passo real para quem vai subir isso hoje.

```markdown
# 🚀 Guia de Deploy

Este guia cobre o deploy da stack **FastAPI + PostgreSQL**.

## 🏗️ Opção 1: PaaS Moderno (Recomendado)
Usaremos **Neon** (Banco) e **Render** (Aplicação). Ambos possuem planos gratuitos generosos.

### Passo 1: Banco de Dados (Neon.tech)
1.  Crie conta no [Neon.tech](https://neon.tech).
2.  Crie um projeto `mesaflow-prod`.
3.  Copie a **Connection String** (ex: `postgres://user:pass@ep-xyz.aws.neon.tech/neondb`).

### Passo 2: Aplicação (Render.com)
1.  Crie conta no Render e conecte seu GitHub.
2.  Crie um **Web Service**.
3.  **Build Command:** `pip install -r requirements.txt`
4.  **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  Vá em **Environment Variables** e adicione:
    *   `DATABASE_URL`: (Cole a string do Neon aqui)
    *   `SECRET_KEY`: (Gere um hash aleatório forte)
    *   `ENVIRONMENT`: `production`

### Passo 3: Migrações
No dashboard do Render (Shell) ou localmente conectado ao banco remoto:
```bash
alembic upgrade head
```

## 🐳 Opção 2: Docker (VPS/DigitalOcean)
Se preferir controle total em uma máquina Linux.

1.  Provisione um servidor Ubuntu com Docker instalado.
2.  Clone o repo.
3.  Crie o `.env` de produção.
4.  Rode: `docker-compose -f docker-compose.prod.yml up -d`
```

---

### 5️⃣ `.env.example` (O Elo Perdido)

Crie este arquivo na raiz.

```ini
# Configurações do Banco de Dados
# Para Docker local, use: postgresql://postgres:postgres@db:5432/mesaflow
DATABASE_URL=postgresql://user:password@localhost:5432/mesaflow_db

# Segurança (Gere uma chave forte em produção: openssl rand -hex 32)
SECRET_KEY=desenvolvimento_apenas_nao_use_em_prod
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações da Aplicação
ENVIRONMENT=development
DEBUG=True
```

---


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
# 🚀 Guia de Deploy MesaFlow (PaaS)

Este documento detalha as configurações recomendadas para deploy em ambientes PaaS como Render.com, Vercel.com e Neon.tech.

## ⚙️ Configurações Essenciais

### 1. Backend (Render.com)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/api/health` (Crucial para monitoramento e zero-downtime deploys)
- **Variáveis de Ambiente:**
    - `DATABASE_URL`: String de conexão do Neon (com pooler).
    - `REDIS_URL`: URL do Redis (Render Redis / Upstash).
    - `SECRET_KEY`: Chave secreta forte (use `openssl rand -hex 32`).
    - `ENVIRONMENT`: `production`

### 2. Banco de Dados (Neon.tech)
- **Connection Pooling:** Ative para maior performance e estabilidade. Use a string de conexão fornecida.

### 3. Frontend (Vercel.com)
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Environment Variables:**
    - `NEXT_PUBLIC_API_URL`: Link da sua API no Render.
    - `NEXT_PUBLIC_WS_URL`: Link do WebSocket do Render.

---
*Documentação Atualizada em 05/01/2026*
# 🚀 Guia de Deploy de Produção (MesaFlow v2.3)

Este guia cobre o deploy da stack **FastAPI + Next.js + PostgreSQL** usando serviços PaaS modernos.

## 1. Banco de Dados (Neon.tech)
O Neon é um Postgres serverless que escala a zero (custo baixo) e suporta branching.

1.  Crie uma conta em [neon.tech](https://neon.tech).
2.  Crie um projeto chamado `mesaflow-prod`.
3.  No Dashboard, copie a **Connection String** (selecione a opção **Pooled connection**).
4.  Valide a conexão localmente:
    ```bash
    python scripts/setup/check_prod_connection.py
    ```

## 2. Backend (Render.com)
O Render hospeda a API Python e gerencia o SSL automaticamente.

1.  Crie uma conta no [render.com](https://render.com).
2.  Conecte seu repositório GitHub/GitLab.
3.  Clique em **New +** -> **Blueprint**.
4.  O Render vai ler o arquivo `render.yaml` do repositório.
5.  **Configure as Variáveis de Ambiente (Environment Variables):**
    *   `DATABASE_URL`: Cole a string do Neon (com `sslmode=require`).
    *   `SECRET_KEY`: Gere uma nova com `python scripts/setup/generate_production_keys.py`.
    *   `REDIS_URL`: (Opcional) URL do Redis (Upstash ou Render Redis). Se vazio, usa memória local.
6.  Clique em **Apply**. O deploy iniciará automaticamente.

## 3. Frontend (Vercel)
A Vercel é a casa do Next.js e oferece a melhor performance de CDN.

1.  Crie uma conta na [vercel.com](https://vercel.com).
2.  Importe o projeto do GitHub.
3.  **Configurações de Build:**
    *   Framework Preset: **Next.js**
    *   Root Directory: `frontend` (Importante!)
4.  **Environment Variables:**
    *   `NEXT_PUBLIC_API_URL`: A URL do seu backend no Render (ex: `https://mesaflow-api.onrender.com/api`).
    *   `NEXT_PUBLIC_WS_URL`: A URL WebSocket (ex: `wss://mesaflow-api.onrender.com/ws`).
5.  Clique em **Deploy**.

## 4. Pós-Deploy (Migração e Seed)
Após o backend estar rodando, você precisa criar as tabelas no banco de produção.

**Opção A: Via Shell do Render (Recomendado)**
1.  No dashboard do Render, vá na aba "Shell" do serviço `mesaflow-api`.
2.  Execute:
    ```bash
    alembic upgrade head
    python scripts/maintenance/seed.py
    ```

**Opção B: Via Máquina Local**
1.  Crie um arquivo `.env.prod` localmente com a `DATABASE_URL` do Neon.
2.  Rode:
    ```bash
    # Linux/Mac
    DATABASE_URL="sua_url_neon" alembic upgrade head
    
    # Windows (PowerShell)
    $env:DATABASE_URL="sua_url_neon"; alembic upgrade head
    ```

## 5. Monitoramento
*   **Logs:** Verifique a aba "Logs" no Render para erros de inicialização.
*   **Health Check:** Acesse `https://sua-api.onrender.com/api/health` para ver o status dos serviços.
