# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-14 19:45:00
# 🚀 Guia de Início Rápido (VS Code / Windows)

Este guia contém os comandos essenciais para operar o ambiente de desenvolvimento do MesaFlow.

## 1. Modo Automático (Recomendado)
Execute o script batch na raiz do projeto:

```powershell
.\dev.bat
```
*Isso abrirá automaticamente as janelas do Backend e Frontend.*

---

## 2. Modo Manual (Passo a Passo)

Se preferir rodar manualmente no terminal do VS Code, utilize **três terminais separados**:

### Terminal 1: Backend (API)
```powershell
# Ativar ambiente virtual
.\.venv\Scripts\activate

# Iniciar servidor (com Hot Reload)
python run.py
```
> **Sucesso:** O terminal mostrará `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2: Frontend (Web)
```powershell
# Entrar na pasta
cd frontend

# Iniciar Next.js
npm run dev
```
> **Sucesso:** O terminal mostrará `Ready in xxxxms` em `http://localhost:3000`

### Terminal 3: Serviços Auxiliares (Redis/Celery)
Se precisar de filas e WebSockets:
```powershell
# Setup inteligente do Redis (Docker)
python scripts/setup/smart_redis_setup.py

# (Opcional) Iniciar Worker Celery
.\.venv\Scripts\activate
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

---

## 3. Comandos Úteis de Manutenção

| Ação | Comando |
| :--- | :--- |
| **Atualizar Dependências** | `pip install -r requirements.txt` |
| **Criar Migração DB** | `alembic revision --autogenerate -m "nome"` |
| **Aplicar Migração DB** | `alembic upgrade head` |
| **Resetar Banco (Seed)** | `python scripts/validar/seed.py` |
| **Checar Integridade** | `python scripts/maintenance/system_integrity_check.py` |
| **Verificar Logs** | `type comunication\error.log` |

---

## 4. Solução de Problemas Comuns

### Erro: `Address already in use`
Algo já está rodando na porta 8000 ou 3000.
**Solução:** Feche os terminais antigos ou mate o processo:
```powershell
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### Erro: `Redis Connection Error`
O Docker não está rodando.
**Solução:** Abra o Docker Desktop e rode `python scripts/setup/smart_redis_setup.py`.
