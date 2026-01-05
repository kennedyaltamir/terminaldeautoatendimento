# 🛠️ Checklist de Infraestrutura (PaaS)

Para garantir que o ambiente de produção no Render.com esteja otimizado, valide os seguintes pontos baseados nas configurações atuais:

### 1. Sinais Vitais (Health Check)
- [ ] **Path:** `/api/health`
- [ ] **Interval:** 30s (Padrão)
- [ ] **Timeout:** 10s (Padrão)
- **Por que:** Garante que o Render não envie tráfego para a API se o banco Neon estiver em manutenção ou o Redis falhar.

### 2. Variáveis de Ambiente (Environment)
- [ ] `ENVIRONMENT`: `production`
- [ ] `DATABASE_URL`: Deve conter o parâmetro `?sslmode=require` (Neon nativo).
- [ ] `PYTHON_VERSION`: `3.11.0` ou superior (Render detecta automaticamente pelo requirements, mas é bom fixar se houver erro).

### 3. Log de Eventos
- [ ] Após mudar o Health Check Path, monitore a aba **Events**.
- [ ] Se o deploy ficar em "Live", a configuração foi um sucesso.
# 🛠️ Checklist de Infraestrutura (Render.com)

Ajuste as configurações no painel conforme o estado real do repositório:

### 1. Build & Deploy
- [x] **Root Directory:** (Vazio)
- [x] **Build Command:** `pip install -r requirements.txt`
- [x] **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2. Sinais Vitais (Health Checks)
- [ ] **Health Check Path:** `/api/health`
- **Importante:** Não use o `/healthz` padrão do Render, pois o nosso endpoint customizado valida também a conexão com o banco Neon.

### 3. Variáveis de Ambiente
- [ ] `DATABASE_URL`: String de conexão do Neon (com pooling).
- [ ] `ENVIRONMENT`: `production`
- [ ] `PYTHON_VERSION`: `3.11.0` ou superior.
# 🛠️ Checklist de Infraestrutura (Render.com) - FINALIZADO

As configurações de Build e Deploy foram validadas e estão prontas para escala.

### 1. Build & Deploy (CONCLUÍDO)
- [x] **Root Directory:** (Vazio - Indica a raiz do repositório)
- [x] **Build Command:** `pip install -r requirements.txt`
- [x] **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2. Sinais Vitais (PENDENTE DE VERIFICAÇÃO NO PAINEL)
- [ ] **Health Check Path:** `/api/health`
- **Atenção:** Verifique se você salvou esta alteração na aba "Settings" logo abaixo da parte de Build.

### 3. Variáveis de Ambiente (Environment)
Certifique-se de que estas chaves estão cadastradas na aba **Environment**:
- [ ] `DATABASE_URL`: (Sua string do Neon)
- [ ] `SECRET_KEY`: (Sua chave JWT)
- [ ] `ENVIRONMENT`: `production`
- [ ] `GOOGLE_CLIENT_ID`: (Para o funcionamento do Login Social)
- [ ] `WHATSAPP_API_URL` e `WHATSAPP_API_TOKEN`: (Para notificações reais)
