# 📱 Task: Correção de Tela em Branco no Expo Web

## 1. Problema
O bundle gerado para a plataforma Web apresentava o erro `Uncaught SyntaxError: Cannot use 'import.meta' outside a module`, resultando em uma tela branca.

## 2. Causa Raiz
Incompatibilidade no perfil de transformação do Metro (`hermes-stable` sendo usado indevidamente na Web) e necessidade de suporte sintático para metadados de módulos no React 19.

## 3. Solução
- Criado `metro.config.js` forçando `unstable_transformProfile = 'default'`.
- Atualizado `babel.config.js` com o plugin de sintaxe `import-meta`.

---
*Manutenção de Infraestrutura — Janeiro de 2026*
