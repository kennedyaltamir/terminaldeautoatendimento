# 🚨 Relatório de Incidente: Erro de Compilação JS (Top Level Export)

**Data:** 10 de Janeiro de 2026  
**Sintoma:** `Compiling JS failed: export declaration must be at top level of module`.

## 1. Diagnóstico da Causa Raiz
O erro foi causado por uma combinação de dois fatores críticos:
1.  **Indentação de Código:** O processo de atualização anterior inseriu espaços em branco antes das palavras-chave `import` e `export`. Em ambientes de "Strict Mode" do React Native 0.76 (Hermes), isso pode fazer com que o parser interprete o arquivo como um script comum em vez de um módulo ES, disparando o erro de "Top Level".
2.  **Conflito de Babel:** A presença de plugins de transformação de módulos CommonJS no `package.json` estava interferindo no `babel-preset-expo`, gerando um bundle final com sintaxe híbrida inválida.
3.  **Erro de Plataforma (Web vs Native):** O uso acidental de tags `<div>` em componentes nativos (`WaiterDashboard`) corrompeu a árvore de renderização.

## 2. Ações de Correção Aplicadas

### 2.1. Limpeza de Dependências (package.json)
Removemos os plugins Babel redundantes que causavam o conflito de transpilação. O `babel-preset-expo` agora é o único responsável pela transformação.

### 2.2. Correção de Sintaxe Nativa
Substituímos todas as ocorrências de `<div>` por `<View>` no `WaiterDashboard.tsx` e corrigimos propriedades de estilo não suportadas (como `p: 10`).

### 2.3. Alinhamento de Módulos (Babel & Metro)
Simplificamos o `babel.config.js` e o `metro.config.js` para garantir que o Metro Bundler trate o projeto como um módulo ES puro, isolando-o de interferências da pasta raiz.

## 3. Plano de Prevenção
- Criado o script `scripts/maintenance/fix_mobile_exports.py` para sanitizar automaticamente qualquer arquivo que apresente indentação em declarações de módulo.
