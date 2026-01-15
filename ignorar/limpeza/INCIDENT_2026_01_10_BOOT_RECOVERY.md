# 🚨 Relatório de Recuperação de Boot: Sintaxe e Conectividade

**Data:** 10 de Janeiro de 2026  
**Status:** CRÍTICO - Ação Necessária

## 1. Diagnóstico da Persistência do Erro
Apesar das aplicações de patch anteriores, o Next.js continua reportando um erro de sintaxe na linha 20 do arquivo `api.ts`. Isso indica que o arquivo em disco **não foi atualizado corretamente** ou o cache do Next.js está ignorando a mudança.

### Erro de Sintaxe (Linha 20):
O código atual está assim:
`options.headers,`
O código correto DEVE ser:
`options.headers,`

## 2. Falha de Autenticação do Banco (Ação Manual Obrigatória)
O log do backend confirma: `FATAL: autenticação do tipo senha falhou para o usuário "postgres"`.
O sistema está tentando conectar com a senha `postgres` (definida no seu `.env`), mas o seu PostgreSQL local está rejeitando.

**👉 AÇÃO:** Você deve abrir o arquivo `.env` na raiz e alterar a `DATABASE_URL`. 
Se você não tem senha no Postgres, use:
`DATABASE_URL=postgresql://postgres@localhost:5432/mesaflow_db`

## 3. Correção de Encoding no Backend
O `UnicodeDecodeError` no `IfoodService` foi causado pela mensagem de erro do Windows (em Português/CP1252) sendo lida como UTF-8. Blindamos o serviço para converter qualquer erro em string segura antes do log.

## 4. Plano de Execução
1. Sobrescrever `api.ts` com a sintaxe garantida.
2. Blindar o `IfoodService` contra erros de decodificação.
3. Forçar a detecção do IP local para garantir que o Mobile e o Web usem a mesma base.
