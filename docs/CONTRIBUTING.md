# docs/CONTRIBUTING.md
```markdown
# 💻 Guia de Contribuição (Developers)

Padrões e processos para manter a qualidade do código do MesaFlow.

---

## 1. Setup do Ambiente

### Backend (Python/FastAPI)
```bash
# 1. Criar venv
python -m venv venv
source venv/bin/activate # ou venv\Scripts\activate no Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Ajuste a DATABASE_URL para seu PostgreSQL local

# 4. Rodar Migrations e Seed
alembic upgrade head
python scripts/seed.py

# 5. Rodar Servidor
python run.py
Frontend (Next.js)
code
Bash
cd frontend
npm install
npm run dev
2. Padrões de Código
Cabeçalho de Arquivo (Obrigatório)
Todo arquivo deve começar com o caminho relativo comentado. Isso é vital para nossos scripts de automação.
code
Python
# app/routers/exemplo.py
Tipagem
Python: Use Type Hints sempre. def func(a: int) -> str:.
TypeScript: Sem any. Defina interfaces em types/index.ts.
Linting
O projeto usa Black (Python) e ESLint (JS/TS).
Não commite código com erros de lint.
3. Fluxo de Testes
Nenhuma feature sobe sem teste.
Crie o arquivo de teste em tests/test_nome_feature.py.
Use pytest e TestClient do FastAPI.
Rode a suíte completa antes do push:
code
Bash
python -m pytest
4. Protocolo de Deploy
Branching: main é produção. Desenvolva em feature/nome-da-feature.
Pull Request: Descreva o que mudou e anexe o print do teste passando.
Migrations: Se alterou o models.py:
code
Bash
alembic revision --autogenerate -m "descricao da mudanca"
alembic upgrade head
Verifique o arquivo de migração gerado antes de commitar.