# 📝 Especificação Técnica: TASK-MAINT-01
> **Título:** Sanitização do Repositório (Limpeza de Lixo Digital)
> **Status:** APROVADO
> **Ação:** MOVER (Nunca Deletar)

## 1. Definição de Lixo (Alvos de Movimentação)
Arquivos que poluem a raiz e dificultam a geração de contexto:
- Padrões de nome: arquivos que começam com temp_ e terminam em .py.
- Padrões de nome: arquivos que começam com old_ e terminam em .md.
- Extensões: .bak, .tmp.
- Logs: arquivos .log (exceto o arquivo atualizar.log).
- Arquivos .txt órfãos na raiz (exceto todososarquivos.txt, requirements.txt, resposta.txt, governance_bundle.txt).
- Scripts de teste soltos na raiz (arquivos que começam com test_ e terminam em .py).
- Arquivos de rascunho ou backups manuais identificados.

## 2. SAFE_LIST (Arquivos Intocáveis)
Estes arquivos e diretórios nunca devem ser movidos:
- Diretórios: app, frontend, mobile, docs, scripts, alembic, .git, .github.
- Kernel: atualizar.py, gerartxt.py, run.py, gerardoc.py, gerar_kernel.py.
- Configuração: requirements.txt, package.json, alembic.ini, docker-compose.yml, Dockerfile, .env, .gitignore, pytest.ini, vercel.json, app.json, eas.json.
- Contexto: todososarquivos.txt, resposta.txt, atualizar.log, governance_bundle.txt.

## 3. Destino
Todos os arquivos identificados como lixo devem ser movidos para o diretório ignorar na raiz do projeto, preservando a estrutura de nomes para possível recuperação.
