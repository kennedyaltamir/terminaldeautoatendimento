# 📱 Task: Resolução Crítica de import.meta no Expo Web

## 1. Diagnóstico
O navegador Chrome/Edge reportava `SyntaxError` ao encontrar `import.meta` dentro do `AppEntry.bundle`. Isso ocorria porque o bundle não é carregado como módulo.

## 2. Solução Implementada
- Substituído plugin de sintaxe por plugin de transformação: `babel-plugin-transform-import-meta`.
- Sincronização do `metro.config.js` para forçar o perfil de transpilação compatível com navegadores.

## 3. Resultado Esperado
Renderização da tela de login no Simple Browser do VS Code e em navegadores externos.

---
*Manutenção de Infraestrutura — Janeiro de 2026*
