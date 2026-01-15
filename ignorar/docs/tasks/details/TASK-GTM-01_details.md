# 🏗️ Detalhamento Técnico: Infraestrutura Blindada (TASK-GTM-01)

## 1. Contexto e Justificativa
A arquitetura atual utiliza conexões diretas com o PostgreSQL. Em ambientes Serverless (Render + Neon), isso causa dois problemas críticos:
1.  **Exaustão de Conexões:** O Render escala horizontalmente (mais instâncias), abrindo novas conexões. O Neon tem um limite rígido no plano gratuito/launch.
2.  **Latência de Handshake:** O SSL Handshake do Postgres é custoso.

A solução é utilizar o **PgBouncer** (Connection Pooling) fornecido pelo Neon e otimizar o SQLAlchemy.

## 2. Especificação de Implementação

### 2.1 Ajuste de Connection String
O sistema deve detectar e forçar o uso do endpoint "pooled" do Neon.
- **Lógica:** Se a URL conter `neon.tech` e não tiver `-pooler`, alertar ou ajustar (se possível via env var).
- **Ação:** Atualizar documentação de deploy para exigir a URL correta.

### 2.2 Otimização do SQLAlchemy (`app/database.py`)
Configurar o `create_engine` com parâmetros agressivos de resiliência:
```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,          # Mantém 20 conexões abertas por worker
    max_overflow=10,       # Permite picos de até 30
    pool_timeout=30,       # Espera 30s antes de dar erro
    pool_pre_ping=True,    # Verifica se a conexão está viva antes de usar (Vital para Neon)
    pool_recycle=1800      # Recicla conexões a cada 30 min
)
```

### 2.3 Configuração do Gunicorn (`render.yaml`)
O servidor de aplicação deve ser configurado para maximizar o uso de CPU do plano Starter.
- **Workers:** `WEB_CONCURRENCY` deve ser definido (padrão: 2-4 workers).
- **Classe:** `uvicorn.workers.UvicornWorker` (já em uso, manter).

## 3. Plano de Validação
Criar script `scripts/production/verify_db_pool.py` que:
1.  Abre 50 threads simultâneas.
2.  Executa `SELECT 1` em cada uma.
3.  Mede o tempo de resposta e taxa de erro.
4.  **Sucesso:** 0 erros e latência média < 200ms.
