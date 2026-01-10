# 🚨 Relatório de Incidente: Erro de Importação no Metro Config

**Data:** 10 de Janeiro de 2026  
**Sintoma:** `TypeError: getDefaultConfig is not a function` ao iniciar o Metro Bundler.

## 1. Diagnóstico da Causa Raiz
O erro ocorre devido a um caminho de importação incorreto no arquivo `mobile/metro.config.js`. 

No Expo SDK 52, a função `getDefaultConfig` deve ser importada do pacote `@expo/metro-config` (ou `expo/metro-config`), e não de `expo/config`. O pacote `expo/config` é utilizado para ler o `app.json`, enquanto o `expo/metro-config` fornece a base de configuração para o bundler.

## 2. Ações de Correção
1.  **Correção do Import:** Alterar a origem de `getDefaultConfig` para o pacote correto.
2.  **Sincronização de Dependências:** Garantir que o pacote `@expo/metro-config` esteja presente no ambiente.

## 3. Comportamento Esperado
Após a correção, o comando `npx expo start` deve carregar o arquivo de configuração sem erros de tipo e iniciar o servidor Metro normalmente.
