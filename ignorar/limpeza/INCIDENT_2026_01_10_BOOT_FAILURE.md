# 🚨 Relatório de Incidente: Falha Crítica de Boot e Compilação

**Data:** 10 de Janeiro de 2026  
**Severidade:** CRÍTICA (Sistema Inoperante)  
**Status:** Diagnóstico Concluído

## 1. Sumário do Erro
O sistema MesaFlow falhou ao inicializar devido a uma cascata de erros em ambos os domínios (Frontend e Backend). O Frontend apresenta um erro de sintaxe que impede a compilação do Next.js, enquanto o Backend sofre de falhas de autenticação de banco de dados e indisponibilidade de infraestrutura (Redis).

## 2. Análise Técnica das Causas Raízes

### 2.1. Erro de Sintaxe no Frontend (`api.ts`)
O arquivo `frontend/src/lib/api.ts` contém uma instrução inválida na linha 20.
- **Causa:** Tentativa de injetar `options.headers` dentro de um objeto literal sem o operador de espalhamento (*spread operator* ``).
- **Impacto:** O compilador SWC do Next.js aborta o build, resultando em Erro 500 em todas as rotas.

### 2.2. Falha de Autenticação no PostgreSQL
O log do Backend revela: `FATAL: autenticação do tipo senha falhou para o usuário "postgres"`.
- **Causa:** A senha definida na variável `DATABASE_URL` no arquivo `.env` não corresponde à senha real do banco de dados local.
- **Impacto:** O sistema não consegue persistir ou ler dados, quebrando o loop de polling do iFood e outras funções core.

### 2.3. Erro de Encoding (UnicodeDecodeError)
O Backend travou ao tentar logar o erro do banco de dados.
- **Causa:** O driver do Postgres retornou uma mensagem com caracteres especiais (ex: "autenticação") em codificação local (CP1252/Windows), e o Python tentou decodificar como UTF-8.
- **Impacto:** Crash do serviço de integração iFood.

### 2.4. Indisponibilidade do Redis
Logs: `Timeout connecting to server`.
- **Causa:** O serviço Redis não está rodando na máquina host ou a porta 6379 está bloqueada.
- **Impacto:** O sistema entra em "Fail-Open", desabilitando a blacklist de tokens e o cache de performance.

## 3. Plano de Correção
1. Aplicar o *spread operator* em `api.ts`.
2. Corrigir o tratamento de exceções no `ifood_service.py` para evitar erros de encoding.
3. Validar credenciais do banco de dados no `.env`.
