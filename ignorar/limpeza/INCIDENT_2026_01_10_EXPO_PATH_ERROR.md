# 🚨 Relatório de Incidente: Erro de Contexto de Diretório (Expo SDK)

**Data:** 10 de Janeiro de 2026  
**Sintoma:** `ConfigError: Cannot determine the project's Expo SDK version`.
**Log de Erro:** `Starting project at C:\mesaflow`

## 1. Diagnóstico da Causa Raiz
O erro ocorre porque o comando `npx expo start` foi executado (ou interpretado) a partir da **raiz do projeto** (`C:\mesaflow`) e não de dentro da pasta **mobile** (`C:\mesaflow\mobile`).

Como existe um arquivo `package.json` na raiz (usado para ferramentas de desenvolvimento do kernel), o Expo tenta iniciar o projeto ali. Porém, o pacote `expo` e as configurações do aplicativo estão localizados exclusivamente na subpasta `mobile/`.

## 2. As 5 Possibilidades de Falha Analisadas

### 2.1. Execução no Diretório Incorreto (Confirmado)
O log mostra explicitamente `Starting project at C:\mesaflow`. O Expo não encontra a dependência `expo` no `package.json` da raiz.

### 2.2. Cache de Terminal (PowerShell)
O prompt duplo no seu log `(.venv) PS C:\mesaflow\mobile> (.venv) PS C:\mesaflow>` sugere que o PowerShell pode estar mantendo um estado de diretório inconsistente ou executando um comando encadeado que volta para a raiz.

### 2.3. Ausência de node_modules na pasta Mobile
Se o `npm install` foi rodado na raiz por engano, a pasta `mobile/node_modules` pode estar vazia ou incompleta.

### 2.4. Conflito de package.json
A presença de um `package.json` na raiz confunde ferramentas de CLI que buscam o arquivo de configuração subindo a árvore de diretórios.

### 2.5. Variáveis de Ambiente de Path
Se houver um processo do Expo travado na raiz, o `npx` pode estar tentando reutilizar esse contexto.

## 3. Plano de Resolução (Execução Obrigatória)
1. Garantir a entrada física na pasta correta.
2. Limpar qualquer processo órfão.
3. Executar o start isolado.
