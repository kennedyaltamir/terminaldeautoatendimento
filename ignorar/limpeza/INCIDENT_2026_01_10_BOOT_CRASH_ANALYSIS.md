# 🚨 Relatório de Incidente: Falha Crítica de Compilação e Conectividade

**Data:** 10 de Janeiro de 2026  
**Severidade:** BLOQUEANTE (Sistema Inoperante)  
**Status:** Diagnóstico e Correção de Emergência

## 1. Diagnóstico da Causa Raiz

### 1.1. Erro de Sintaxe no Frontend (`api.ts`)
O compilador Next.js (SWC) falhou ao processar o arquivo `frontend/src/lib/api.ts`.
- **Evidência:** `Expected a semicolon` na linha 20.
- **Causa:** O arquivo continha a instrução `options.headers,` dentro de um objeto. Em TypeScript, isso é interpretado como uma tentativa de declarar uma propriedade sem valor, o que exige um ponto e vírgula. A intenção correta era usar o **spread operator** (`options.headers`) para mesclar os cabeçalhos.
- **Efeito Cascata:** A falha de sintaxe corrompeu a árvore de tipos, gerando erros falsos de "propriedade desconhecida" nas chamadas de `fetch` subsequentes.

### 1.2. Falha de Autenticação no PostgreSQL
O log do Backend revela: `FATAL: autenticação do tipo senha falhou para o usuário "postgres"`.
- **Causa:** O arquivo `.env` está configurado com a senha `postgres`, mas o serviço PostgreSQL instalado na máquina host Windows está configurado com uma senha diferente ou sem senha.

### 1.3. UnicodeDecodeError no iFood Service
O Backend sofreu um crash ao tentar logar a falha do banco de dados.
- **Causa:** O driver do Postgres retornou o erro em Português (codificação CP1252/Windows). O Python tentou decodificar como UTF-8 e falhou no caractere "ç" de "autenticação".

## 2. Plano de Resolução Aplicado

1.  **Sanitização de Sintaxe:** Reconstrução integral do `api.ts` com spread operators corretos e remoção de qualquer comentário estilo Python (`#`).
2.  **Blindagem de Logs:** Atualização do `IfoodService` para tratar erros de decodificação de forma segura.
3.  **Ferramenta de Diagnóstico:** Criação do `full_system_check.py` para validar os 5 pontos críticos de falha.
