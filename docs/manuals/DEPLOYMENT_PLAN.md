# 🚀 Plano de Implantação (Deployment Plan)

Este documento guia a instalação do MesaFlow em um novo ambiente de produção.

## 1. Pré-requisitos de Infraestrutura
- **PaaS:** Conta no Render.com (ou AWS/DigitalOcean).
- **Database:** PostgreSQL gerenciado (Neon.tech recomendado).
- **Cache:** Redis gerenciado (Upstash recomendado).
- **Domínio:** Acesso ao DNS para configurar CNAME.

## 2. Configuração de Variáveis (.env)
As seguintes chaves são obrigatórias no ambiente de produção:

```ini
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
REDIS_URL=redis://default:pass@host:port
SECRET_KEY=hash_super_seguro_gerado_com_openssl
NEXT_PUBLIC_API_URL=https://api.seudominio.com/api
NEXT_PUBLIC_WS_URL=wss://api.seudominio.com/ws
```

## 3. Procedimento de Deploy (Zero Downtime)

### Backend (API)
1.  Push para a branch `main`.
2.  O GitHub Actions roda os testes (`pytest`).
3.  Se passar, o Render faz o pull e build (`pip install`).
4.  **Migração:** O comando de start deve incluir `alembic upgrade head` antes de subir o servidor, ou isso deve ser rodado manualmente no console.

### Frontend (Web)
1.  O Vercel detecta o push na `main`.
2.  Executa `npm run build`.
3.  Promove a nova versão para a Edge Network.

## 4. Plano de Rollback
Em caso de falha crítica após o deploy:
1.  **Frontend:** No painel da Vercel, clique em "Instant Rollback" para a versão anterior.
2.  **Backend:** No Render, selecione o deploy anterior e clique em "Rollback".
3.  **Banco de Dados:** Se houve migração destrutiva, restaure o backup do Neon (Time Travel) para o ponto antes do deploy.
