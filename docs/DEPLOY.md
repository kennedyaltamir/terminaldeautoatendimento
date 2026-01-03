
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
